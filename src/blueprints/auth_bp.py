# auth_bp.py
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request, jsonify, abort
from app import db, bcrypt, jwt
from models.user import User, UserSchema
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

# Creating a Blueprint for authentication-related routes
auth_blueprint = Blueprint('auth', __name__)

def admin_required():
    # A decorator function to check if the current user is an admin
    jwt_user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=jwt_user_id)
    user = db.session.scalar(stmt)
    if not (user and user.is_admin):
        # Abort the request with a 401 Unauthorized if the user is not an admin
        abort(401)

@auth_blueprint.route('/register', methods=['POST'])
def register():
    # Endpoint to register a new user
    user_schema = UserSchema()
    try:
        # Load and validate the user data from the request
        user_data = user_schema.load(request.json)
        # Hash the user's password for security
        hashed_password = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
        # Create a new User object and add it to the database
        new_user = User(username=user_data['username'], email=user_data['email'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        # Return the user data, excluding sensitive information like password and admin status
        return UserSchema(exclude=["password", "is_admin"]).dump(new_user), 201
    except IntegrityError:
        # Return an error if the user already exists (e.g., duplicate email)
        return {'error': 'User already exists'}, 409

@auth_blueprint.route('/login', methods=['POST'])
def login():
    # Endpoint for user login
    user_schema = UserSchema(only=["email", "password"])
    try:
        # Load and validate the login data from the request
        user_data = user_schema.load(request.json)
        # Find the user by email
        user = User.query.filter_by(email=user_data['email']).first()
        # Check if the user exists and the password is correct
        if user and bcrypt.check_password_hash(user.password, user_data['password']):
            # Generate a JWT token for the user
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token), 200
        else:
            # Return an error if the login credentials are invalid
            return {'error': 'Invalid email address or password'}, 401
    except KeyError:
        # Return an error if the email or password is missing from the request
        return {'error': 'Email and password are required'}, 400

@auth_blueprint.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    # Endpoint to list all users (admin only)
    admin_required()
    # Retrieve all users from the database
    users = User.query.all()
    # Serialize the user data and return it
    user_schema = UserSchema(many=True)
    return jsonify(user_schema.dump(users)), 200

@auth_blueprint.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    # Endpoint to get a specific user's details (admin only)
    admin_required()
    # Retrieve the user by their ID
    user = User.query.get(user_id)
    if user:
        # Serialize and return the user data if found
        user_schema = UserSchema()
        return jsonify(user_schema.dump(user)), 200
    else:
        # Return a not found message if the user does not exist
        return jsonify({"message": "User not found"}), 404

@auth_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    # Endpoint to delete a specific user (admin only)
    admin_required()
    # Retrieve the user by their ID
    user = User.query.get(user_id)
    if user:
        # Delete the user from the database and commit the changes
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        # Return a not found message if the user does not exist
        return jsonify({"message": "User not found"}), 404
