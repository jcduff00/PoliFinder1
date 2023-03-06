from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from polifinder_app.models import Politician, District, User
from polifinder_app.main.forms import PoliticianForm, DistrictForm

from polifinder_app.extensions import app, db, bcrypt

main = Blueprint("main", __name__)

def init_db():
    db.drop_all()
    db.create_all()

    a1 = District(name='MI05', state='Michigan', region='Midwest')
    db.session.add(a1)

    a2 = District(name='NJ03', state='New Jersey', region='Midatlantic')
    db.session.add(a2)

    a3 = District(name='FL01', state='Florida', region='Southeast')
    db.session.add(a3)

    a4 = District(name='OK05', state='Oklahoma', region='Southwest')
    db.session.add(a4)

    a5 = District(name='WA09', state='Washington', region='Northwest')
    db.session.add(a5)

    b1 = Politician(
            name = 'Justin Amash',
            office = 'Congressman',
            party = 'LIBERTARIAN',
            photo_url = "test",
            district = a1
    )
    db.session.add(b1)

    b2 = Politician( 
        name = 'Andy Kim', 
        office = 'Congressman', 
        party = 'DEMOCRATIC', 
        photo_url = "test", 
        district = a2
    )
    db.session.add(b2)

    b3 = Politician( 
        name = 'Matt Gaetz', 
        office = 'Congressman', 
        party = 'REPUBLICAN', 
        photo_url = "test", 
        district = a3
    )
    db.session.add(b3)

    b4 = Politician( 
        name = 'Stephanie Bice', 
        office = 'Congresswoman',
        party = 'REPUBLICAN', 
        photo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Rep._Stephanie_Bice%2C_117th_Congress.jpg/1200px-Rep._Stephanie_Bice%2C_117th_Congress.jpg", 
        district = a4
    )
    db.session.add(b4) 

    b5 = Politician( 
        name = 'Pramila Jayapal',
        office = 'Congresswoman', 
        party = 'DEMOCRATIC', 
        photo_url = "test", 
        district = a5
    )
    db.session.add(b5) 

    u1 = User(
        username="test-user",
        password=bcrypt.generate_password_hash("password").decode('utf-8')
    )
    db.session.add(u1)

    db.session.commit()

init_db()

##########################################
#           Routes                       #
##########################################

@main.route('/')
def home():
    all_politicians = Politician.query.all()
    print(all_politicians)
    return render_template('home.html', all_politicians=all_politicians)

@main.route('/new_politician', methods=['GET', 'POST'])
@login_required
def new_politician():

    form = PoliticianForm()

    if form.validate_on_submit(): 
        new_politician = Politician(
            name = form.name.data, 
            office = form.office.data, 
            party = form.party.data,
            photo_url = form.photo_url.data,
            district = form.district.data
        )
        db.session.add(new_politician)
        db.session.commit()
             
        flash('Politician added to our roster. Thank you!')
        return redirect(url_for('main.politician_detail', politician_id = new_politician.id))
    else: 
        return render_template('new_politician.html', form=form)

@main.route('/new_district', methods=['GET', 'POST'])
@login_required
def new_district():

    form = DistrictForm()

    if form.validate_on_submit(): 
         new_district = District(
              name = form.name.data, 
              state = form.state.data,
              region = form.region.data
         )
         db.session.add(new_district)
         db.session.commit()

         flash('District added to our list. Thank you!')
         return redirect(url_for('main.home'))
    else: 
         return render_template('new_district.html', form=form)

@main.route('/politician/<politician_id>', methods=['GET', 'POST'])
@login_required
def politician_detail(politician_id):
    politician = Politician.query.get(politician_id)
    form = PoliticianForm(obj=politician)

    if form.validate_on_submit(): 
        politician.name = form.name.data
        politician.office = form.office.data
        politician.party = form.party.data
        politician.photo_url = form.photo_url.data
        politician.district = form.district.data
        db.session.commit()

        flash('This politician information has been updated. Thank you!')
        return redirect(url_for('main.politician_detail', politician_id = politician_id))
    else: 
        return render_template('politician_detail.html', politician=politician, form=form)

@main.route('/profile/<username>')
def profile(username):
    all_politicians = Politician.query.all()
    user = Politician.query.filter_by(username=username).first()
    favorite_politicians_list = user.favorite_politician

    return render_template('profile.html', user=user, all_politicians=all_politicians, favorite_politicians_list=favorite_politicians_list)
