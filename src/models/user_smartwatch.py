from init import db, ma
from marshmallow import fields

from app import db

class UserSmartwatch(db.Model):
    __tablename__ = 'user_smartwatches'
    id = db.Column(db.Integer, primary_key=True)
    smartwatch_id = db.Column(db.Integer, db.ForeignKey('smartwatches.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    smartwatch = db.relationship('Smartwatch', back_populates='users')
    user = db.relationship('User', back_populates='smartwatches')

class UserSmartwatchSchema(ma.Schema):
    class Meta:
        fields = ('id', 'smartwatch_id', 'user_id')
