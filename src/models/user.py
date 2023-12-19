# user.py
from app import db, ma
from marshmallow import fields
from marshmallow.validate import Length

# Define User model for database
class User(db.Model):
    __tablename__ = "users"
    # Define model fields
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    # Relationship with UserSmartwatch for referencing smartwatches
    smartwatches = db.relationship('UserSmartwatch', back_populates='user', cascade="all, delete-orphan")

# Marshmallow schema for User model for serialization/deserialization and validation
class UserSchema(ma.Schema):
    id = fields.Integer()
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=Length(min=8, error='Password must be at least 8 characters'))
    class Meta:
        fields = ("id", "username", "email", "password", "is_admin")
