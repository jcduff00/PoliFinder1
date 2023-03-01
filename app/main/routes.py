from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from app.models import Politician, District, User
from main.forms import PoliticianForm, DistrictForm

from app.extensions import app, db
import bcrypt

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_politicians = Politician.query.all()
    print(all_politicians)
    return render_template('home.html', all_politicians=all_politicians)

@main.route('/new_politician', methods=['GET', 'POST'])
@login_required
def new_politician():

    form = PoliticianForm()

    if form.validate_on_submit(): 
        new_store = Politician(
            name = form.name.data, 
            office = form.office.data, 
            party = form.party.data,
            photo_url = form.photo_url.data,
            district_id = form.district.data
        )

        db.session.add(new_politician)
        db.session.commit()
             
        flash('Politician added to our roster. Thank you!')
        return redirect(url_for('main.politician_detail', politician_id = new_politician))
    else: 
        return render_template('new_politician.html')

@main.route('/new_district', methods=['GET', 'POST'])
@login_required
def new_district():

    form = DistrictForm()

    if form.validate_on_submit(): 
         new_item = District(
              name = form.name.data, 
              state = form.state.data,
              region = form.region.data
         )

         db.session.add(new_item)
         db.session.commit()

         flash('District added to our list. Thank you!')
         return redirect(url_for('main.district_detail', district_id = new_district.id))
    else: 
         return render_template('new_district.html', form = form)

@main.route('/district/<district_id>', methods=['GET', 'POST'])
@login_required
def district_detail(district_id):
    district = District.query.get(district_id)
    form = DistrictForm(obj=district)

    if form.validate_on_submit(): 
        form.populate_obj(district)
        db.session.add(district)
        db.session.commit()

        flash('Your district has been validated and updated. Thank you!')
        return redirect(url_for('main.district_detail', district_id = district))
    else: 
        district = District.query.get(district_id)
        return render_template('district_detail.html', district=district)

@main.route('/politician/<politician_id>', methods=['GET', 'POST'])
@login_required
def politician_detail(politician_id):
    politician = Politician.query.get(politician_id)
    form = PoliticianForm(obj=politician)

    if form.validate_on_submit(): 
        form.populate_obj(politician)
        db.session.add(politician)
        db.session.commit()

        flash('This politician information has been updated. Thank you!')
        return redirect(url_for('main.politician_detail', politician_id = politician))
    else: 
        item = Politician.query.get(politician_id)
        return render_template('politician_detail.html', politician=politician)