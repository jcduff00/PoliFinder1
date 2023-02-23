# Create your models here.
from sqlalchemy_utils import URLType
from app.extensions import db
from datetime import date

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

class Politician(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    office = db.Column(db.String, nullable=False)
    elected_date = db.Column(db.Date, nullable=False)

class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    
    zipcode = db.Column(db.Integer, nullable=False)

