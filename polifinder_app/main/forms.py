from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from polifinder_app.models import Politician, District

class DistrictForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    region = SelectField('Region', validators=[DataRequired()])
    submit = SubmitField('Submit')

    pass

class PoliticianForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    office = StringField('Office',validators=[DataRequired()])
    party = SelectField('Party', validators=[DataRequired()])
    photo_url = StringField('Photo_Url', validators=[DataRequired()])
    district = QuerySelectField('District', query_factory=lambda: District.query, validators=[DataRequired()])
    submit = SubmitField('Submit')

    pass