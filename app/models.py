# Create your models here.
from sqlalchemy_utils import URLType
from app.extensions import db
from datetime import date

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String, nullable=False)

class Politician(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    office = db.Column(db.String, nullable=False)
    elected_date = db.Column(db.Date, nullable=False)
    users = db.relationship('User', 
        secondary='politician_user', back_populates='politicians')
    districts = db.relationship('District', 
        secondary='politician_district_table', back_populates='politicians')

class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String, nullable=False)
    users = db.relationship('User',
        secondary='district_user', back_populates='districts')
    politicians = db.relationship('Politician',
        secondary='politician_district', back_populates='districts')

politician_user_table = db.Table('politician_user',
    db.Column('politician_id', db.Integer, db.ForeignKey('politician.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

district_user_table = db.Table('district_user',
    db.Column('district_id', db.Integer, db.ForeignKey('district.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

politician_district_table = db.Table('politician_district',
    db.Column('politician_id', db.Integer, db.ForeignKey('politician.id')),
    db.Column('district_id', db.Integer, db.ForeignKey('district.id'))
)



