# user_smartwatches.py
from app import db, ma
from marshmallow import fields

# Define UserSmartwatch model for database
class UserSmartwatch(db.Model):
    __tablename__ = 'user_smartwatches'
    # Define model fields
    id = db.Column(db.Integer, primary_key=True)
    smartwatch_id = db.Column(db.Integer, db.ForeignKey('smartwatches.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    # Relationship with Smartwatch and User models
    smartwatch = db.relationship('Smartwatch', back_populates='users')
    user = db.relationship('User', back_populates='smartwatches')

# Marshmallow schema for UserSmartwatch model
class UserSmartwatchSchema(ma.Schema):
    id = fields.Integer()
    smartwatch_id = fields.Integer()
    user_id = fields.Integer()
    class Meta:
        fields = ('id', 'smartwatch_id', 'user_id')
