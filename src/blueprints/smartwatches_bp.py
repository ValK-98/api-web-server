from flask import Blueprint, request, jsonify, abort
from app import db
from blueprints.auth_bp import admin_required
from models.smartwatch import Smartwatch, SmartwatchSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow.exceptions import ValidationError
from models.user import User 

smartwatch_bp = Blueprint('smartwatches', __name__)
smartwatch_schema = SmartwatchSchema()
smartwatches_schema = SmartwatchSchema(many=True)


@smartwatch_bp.route('/smartwatches', methods=['GET'])
@jwt_required()
def get_smartwatches():
    query = Smartwatch.query
    budget = request.args.get('budget')
    battery_life = request.args.get('battery_life')
    main_feature = request.args.get('main_feature')
    name = request.args.get('name')
    brand = request.args.get('brand')
    year_released = request.args.get('year_released')

    if budget:
        query = query.filter(Smartwatch.budget == budget)
    if battery_life:
        query = query.filter(Smartwatch.battery_life == battery_life)
    if main_feature:
        query = query.filter(Smartwatch.main_feature.ilike(f'%{main_feature}%'))
    if name:
        query = query.filter(Smartwatch.name.ilike(f'%{name}%'))
    if brand:
        query = query.filter(Smartwatch.brand.ilike(f'%{brand}%'))

    try:
        if year_released:
            query = query.filter(Smartwatch.year_released == int(year_released))
    except ValueError:
        return jsonify({"error": "Invalid year format"}), 400

    smartwatches = query.all()
    return jsonify(smartwatches_schema.dump(smartwatches)), 200

@smartwatch_bp.route('/smartwatches/<int:model_id>', methods=['GET'])
@jwt_required()
def get_smartwatch(model_id):
    smartwatch = Smartwatch.query.get_or_404(model_id)
    return jsonify(smartwatch_schema.dump(smartwatch)), 200

@smartwatch_bp.route('/smartwatches', methods=['POST'])
@jwt_required()
def create_smartwatch():
    admin_required()
    try:
        smartwatch_data = smartwatch_schema.load(request.json)
        new_smartwatch = Smartwatch(**smartwatch_data)
        db.session.add(new_smartwatch)
        db.session.commit()
        return jsonify(smartwatch_schema.dump(new_smartwatch)), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

@smartwatch_bp.route('/smartwatches/<int:model_id>', methods=['PUT'])
@jwt_required()
def update_smartwatch(model_id):
    admin_required()
    smartwatch = Smartwatch.query.get_or_404(model_id)
    try:
        updated_data = smartwatch_schema.load(request.json)
        for key, value in updated_data.items():
            setattr(smartwatch, key, value)
        db.session.commit()
        return jsonify(smartwatch_schema.dump(smartwatch)), 200
    except ValidationError as err:
        return jsonify(err.messages), 400

@smartwatch_bp.route('/smartwatches/<int:model_id>', methods=['DELETE'])
@jwt_required()
def delete_smartwatch(model_id):
    admin_required()
    smartwatch = Smartwatch.query.get_or_404(model_id)
    db.session.delete(smartwatch)
    db.session.commit()
    return jsonify({"message": "Smartwatch deleted successfully"}), 200
