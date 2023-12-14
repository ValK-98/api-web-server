from app import db, ma
from marshmallow import fields
from marshmallow.validate import Length


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)



class UserSchema(ma.Schema):
    id = fields.Integer()
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=Length(min=8, error='Password must be at least 8 characters'))

    class Meta:
        fields = ("id", "username", "email", "password", "is_admin")