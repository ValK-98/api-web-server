# Importing necessary modules and models
from flask import Blueprint, request, jsonify
from app import db
from models.user_smartwatch import UserSmartwatch, UserSmartwatchSchema
from models.user import User
from models.smartwatch import Smartwatch, SmartwatchSchema
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import admin_required
from sqlalchemy import and_ 

# Creating a Blueprint for user smartwatch related routes
user_smartwatches_bp = Blueprint('user_smartwatches', __name__)

@user_smartwatches_bp.route('/user_smartwatches', methods=['POST'])
@jwt_required()
def add_smartwatch_to_user():
    """
    Endpoint to add a smartwatch to a user's collection.
    Requires JWT authentication. If no optional filter fields are provided, 
    'smartwatch_id' becomes a mandatory field.
    """
    user_id = get_jwt_identity()

    data = request.json
    smartwatch_id = data.get('smartwatch_id')
    filter_fields = ['budget', 'battery_life', 'main_feature', 'name', 'brand', 'year_released']
    filters = {field: data.get(field) for field in filter_fields if data.get(field) is not None}

    # If no filters and no smartwatch_id are provided, return an error
    if not filters and not smartwatch_id:
        return jsonify({"error": "No filters provided. 'smartwatch_id' is required"}), 400

    # If filters are provided, use them to query the smartwatch
    if filters:
        query = Smartwatch.query
        for attr, value in filters.items():
            if attr in ['name', 'brand', 'main_feature']:
                query = query.filter(getattr(Smartwatch, attr).ilike(f'%{value}%'))
            elif attr == 'year_released':
                query = query.filter(getattr(Smartwatch, attr) == int(value))
            else:
                query = query.filter(getattr(Smartwatch, attr) == value)
        smartwatch = query.first()
    else:
        # If only smartwatch_id is provided, query by id
        smartwatch = Smartwatch.query.get(smartwatch_id)

    # Check if the smartwatch exists
    if not smartwatch:
        return jsonify({"error": "Smartwatch not found"}), 404

    # Check if the smartwatch is already in the user's collection
    if UserSmartwatch.query.filter(and_(UserSmartwatch.user_id == user_id, UserSmartwatch.smartwatch_id == smartwatch.id)).first():
        return jsonify({"error": "Smartwatch already added to user's collection"}), 400

    # Add the smartwatch to the user's collection and commit the transaction
    user_smartwatch = UserSmartwatch(user_id=user_id, smartwatch_id=smartwatch.id)
    db.session.add(user_smartwatch)
    db.session.commit()

    return jsonify({"message": "Smartwatch added to user's collection"}), 201


@jwt_required()
def get_smartwatch_data(user_smartwatches):
    """
    Retrieves detailed data of smartwatches for the given user smartwatches.
    """
    smartwatches = []
    for user_smartwatch in user_smartwatches:
        smartwatch = Smartwatch.query.get(user_smartwatch.smartwatch_id)
        smartwatches.append({
            "id": smartwatch.id,
            "name": smartwatch.name,
            "brand": smartwatch.brand,
            "year_released": smartwatch.year_released,
            "budget": smartwatch.budget,
            "battery_life": smartwatch.battery_life,
            "main_feature": smartwatch.main_feature
        })
    return smartwatches

@user_smartwatches_bp.route('/user_smartwatches', methods=['GET'])
@jwt_required()
def get_user_smartwatches():
    """
    Endpoint to get the smartwatches of the currently authenticated user.
    Requires JWT authentication.
    """
    user_id = get_jwt_identity()
    user_smartwatches = UserSmartwatch.query.filter_by(user_id=user_id).all()
    smartwatches = get_smartwatch_data(user_smartwatches)
    return jsonify(SmartwatchSchema(many=True).dump(smartwatches)), 200

@user_smartwatches_bp.route('/user_smartwatches/users/all', methods=['GET'])
@jwt_required()
def get_all_users_smartwatches():
    """
    Endpoint to get smartwatches of all users. 
    Requires JWT authentication and admin privileges.
    """
    admin_required()
    user_smartwatches = UserSmartwatch.query.all()
    smartwatches = get_smartwatch_data(user_smartwatches)
    return jsonify(smartwatches), 200

@user_smartwatches_bp.route('/user_smartwatches/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_specific_user_smartwatches(user_id):
    """
    Endpoint to get the smartwatches of a specific user.
    Requires JWT authentication and admin privileges.
    """
    admin_required()
    user_smartwatches = UserSmartwatch.query.filter_by(user_id=user_id).all()
    smartwatches = get_smartwatch_data(user_smartwatches)
    return jsonify(smartwatches), 200

@user_smartwatches_bp.route('/user_smartwatches/<int:smartwatch_id>', methods=['DELETE'])
@jwt_required()
def delete_user_smartwatch(smartwatch_id):
    """
    Endpoint to remove a smartwatch from the currently authenticated user's collection.
    Requires JWT authentication.
    """
    user_id = get_jwt_identity()
    user_smartwatch = UserSmartwatch.query.filter_by(user_id=user_id, smartwatch_id=smartwatch_id).first()

    # Check if the smartwatch exists in the user's collection
    if not user_smartwatch:
        return jsonify({"error": "Smartwatch not found in user's collection"}), 404

    # Remove the smartwatch from the user's collection and commit the transaction
    db.session.delete(user_smartwatch)
    db.session.commit()

    return jsonify({"message": "Smartwatch removed from user's collection"}), 200
