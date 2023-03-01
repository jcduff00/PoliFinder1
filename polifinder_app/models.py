from sqlalchemy_utils import URLType
from polifinder_app.extensions import db
import enum
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    favorite_politicians_list = db.relationship(
        'Politician', secondary='favorite_politician', back_populates='users_who_favorited')

class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(80), nullable=False)
    region = db.Column(db.String(200), nullable=False)
    politician = db.relationship('Politician', back_populates='district')

class PoliticianParty(enum.Enum): 
    DEMOCRATIC = "Democratic"
    REPUBLICAN = "Republican"
    LIBERTARIAN = "Libertarian"
    GREEN = "Green"
    OTHER = "Other"

class Politician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    office = db.Column(db.String(100), nullable=False)
    party = db.Column(db.Enum(PoliticianParty), default=PoliticianParty.OTHER)
    photo_url = db.Column(URLType)
    district_id = db.Column(
        db.Integer, db.ForeignKey('district.id'), nullable=False)
    district = db.relationship('District', back_populates='politician')
    users_who_favorited = db.relationship('User', secondary='favorite_politician', back_populates='favorite_politicians_list')

favorite_politicians_table = db.Table('favorite_politician', 
    db.Column('politician_id', db.Integer, db.ForeignKey('politician.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)