from marshmallow.exceptions import ValidationError
from flask import Blueprint, request, jsonify, abort
from app import db, bcrypt, jwt
from models.user import User, UserSchema
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


auth_blueprint = Blueprint('auth', __name__)


def admin_required():
    jwt_user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=jwt_user_id)
    user = db.session.scalar(stmt)
    if not (user and user.is_admin):
        abort(401)

@auth_blueprint.route('/register', methods=['POST'])
def register():
    user_schema = UserSchema()
    try:
        user_data = user_schema.load(request.json)
        hashed_password = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
        new_user = User(username=user_data['username'], email=user_data['email'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except ValidationError as err:
        return jsonify(err.messages), 400


@auth_blueprint.route('/login', methods=['POST'])
def login():
    user_schema = UserSchema(only=["email", "password"])
    try:
        user_data = user_schema.load(request.json)
        user = User.query.filter_by(email=user_data['email']).first()
        if user and bcrypt.check_password_hash(user.password, user_data['password']):
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    except ValidationError as err:
        return jsonify(err.messages), 400

