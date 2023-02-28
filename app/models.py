from sqlalchemy_utils import URLType

from app.extensions import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    favorite_politicians_list = db.relationship(
        'Item', secondary='user_politician', back_populates='politicians')

class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    region = db.Column(db.String(200), nullable=False)
    politicians = db.relationship('Politician', back_populates='district')

class Politician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    office = db.Column(db.String(100), nullable=False)
    party = db.Column(db.Enum(PoliticianParty), default=PoliticianCategory.OTHER)
    photo_url = db.Column(URLType)
    state_id = db.Column(
        db.Integer, db.ForeignKey('district.id'), nullable=False)
    state = db.relationship('District', back_populates='politicians')

favorite_politicians_table = db.Table('user_politician', 
    db.Column('politician_id', db.Integer, db.ForeignKey('politician.id'))
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)