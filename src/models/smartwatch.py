# smartwatches.py
from app import db, ma
from marshmallow import fields

# Define Smartwatch model for database
class Smartwatch(db.Model):
    __tablename__ = 'smartwatches'
    # Define model fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    brand = db.Column(db.String, nullable=False)
    year_released = db.Column(db.Integer, nullable=False)
    budget = db.Column(db.String, nullable=False)
    battery_life = db.Column(db.Integer, nullable=False)
    main_feature = db.Column(db.String, nullable=False)
    # Relationship with UserSmartwatch for referencing users
    users = db.relationship('UserSmartwatch', back_populates='smartwatch', cascade="all, delete-orphan")

# Marshmallow schema for Smartwatch model
class SmartwatchSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    brand = fields.Str(required=True)
    year_released = fields.Int(required=True)
    budget = fields.Str(required=True)
    battery_life = fields.Int(required=True)
    main_feature = fields.Str(required=True)
    class Meta:
        fields = ('id', 'name', 'brand', 'year_released', 'budget', 'battery_life', 'main_feature')
