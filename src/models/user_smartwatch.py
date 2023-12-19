from app import db, ma
from marshmallow import fields

class UserSmartwatch(db.Model):
    __tablename__ = 'user_smartwatches'
    id = db.Column(db.Integer, primary_key=True)
    smartwatch_id = db.Column(db.Integer, db.ForeignKey('smartwatches.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    smartwatch = db.relationship('Smartwatch', back_populates='users')
    user = db.relationship('User', back_populates='smartwatches')

class UserSmartwatchSchema(ma.Schema):
    id = fields.Integer()
    smartwatch_id = fields.Integer()
    user_id = fields.Integer()
    class Meta:
        fields = ('id', 'smartwatch_id', 'user_id')
