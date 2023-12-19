from flask import Blueprint, request, jsonify
from app import db
from models.user_smartwatch import UserSmartwatch, UserSmartwatchSchema
from models.user import User
from models.smartwatch import Smartwatch, SmartwatchSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import admin_required
from sqlalchemy import and_ 

user_smartwatches_bp = Blueprint('user_smartwatches', __name__)

@user_smartwatches_bp.route('/user_smartwatches', methods=['POST'])
@jwt_required()
def add_smartwatch_to_user():
    user_id = get_jwt_identity()

    query = Smartwatch.query
    for attr in ['budget', 'battery_life', 'main_feature', 'name', 'brand', 'year_released']:
        if value := request.json.get(attr):
            if attr in ['name', 'brand', 'main_feature']:
                query = query.filter(getattr(Smartwatch, attr).ilike(f'%{value}%'))
            elif attr == 'year_released':
                query = query.filter(getattr(Smartwatch, attr) == int(value))
            else:
                query = query.filter(getattr(Smartwatch, attr) == value)

    smartwatch = query.first()
    if not smartwatch:
        return jsonify({"error": "Smartwatch not found"}), 404

    if UserSmartwatch.query.filter(and_(UserSmartwatch.user_id == user_id, UserSmartwatch.smartwatch_id == smartwatch.id)).first():
        return jsonify({"error": "Smartwatch already added to user's collection"}), 400

    user_smartwatch = UserSmartwatch(user_id=user_id, smartwatch_id=smartwatch.id)
    db.session.add(user_smartwatch)
    db.session.commit()

    return jsonify({"message": "Smartwatch added to user's collection"}), 201

@jwt_required()
def get_smartwatch_data(user_smartwatches):
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
    user_id = get_jwt_identity()
    user_smartwatches = UserSmartwatch.query.filter_by(user_id=user_id).all()
    smartwatches = get_smartwatch_data(user_smartwatches)
    return jsonify(SmartwatchSchema(many=True).dump(smartwatches)), 400

@user_smartwatches_bp.route('/user_smartwatches/users/all', methods=['GET'])
@jwt_required()
def get_all_users_smartwatches():
    admin_required()
    user_smartwatches = UserSmartwatch.query.all()
    smartwatches = get_smartwatch_data(user_smartwatches)
    return jsonify(smartwatches), 200

@user_smartwatches_bp.route('/user_smartwatches/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_specific_user_smartwatches(user_id):
    admin_required()
    user_smartwatches = UserSmartwatch.query.filter_by(user_id=user_id).all()
    smartwatches = get_smartwatch_data(user_smartwatches)
    return jsonify(smartwatches), 200

@user_smartwatches_bp.route('/user_smartwatches/<int:smartwatch_id>', methods=['DELETE'])
@jwt_required()
def delete_user_smartwatch(smartwatch_id):
    user_id = get_jwt_identity()
    user_smartwatch = UserSmartwatch.query.filter_by(user_id=user_id, smartwatch_id=smartwatch_id).first()

    if not user_smartwatch:
        return jsonify({"error": "Smartwatch not found in user's collection"}), 404

    db.session.delete(user_smartwatch)
    db.session.commit()

    return jsonify({"message": "Smartwatch removed from user's collection"}), 200