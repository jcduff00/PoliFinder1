from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from app.models import Politician, District, User
from main.forms import PoliticianForm, DistrictForm, LoginForm, SignUpForm

from app.extensions import app, db
import bcrypt

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_suits = Politician.query.all()
    print(all_politicians)
    return render_template('home.html', all_politicians=all_politicians)

@main.route('/new_store', methods=['GET', 'POST'])
@login_required
def new_store():

    form = PoliticianForm()

    if form.validate_on_submit(): 
        new_store = Politician(
            title = form.title.data, 
            address = form.address.data 
        )

        db.session.add(new_store)
        db.session.commit()
             
        flash('This store has been added. Thank you!')
        return redirect(url_for('main.store_detail', politician_id = new_politician))
    else: 
        return render_template('new_store.html')

@main.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():

    form = GroceryItemForm()

    if form.validate_on_submit(): 
         new_item = GroceryItem(
              name = form.name.data, 
              price = form.price.data, 
              category = form.category.data, 
              photo_url = form.photo_url.data, 
              store_id = form.store.data
              created_by = current_user
         )

         db.session.add(new_item)
         db.session.commit()

         flash('This item has been added. Thank you!')
         return redirect(url_for('main.item_detail', item_id = new_item.id))
    else: 
         return render_template('new_item.html', form = form)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
@login_required
def store_detail(store_id):
    store = GroceryStore.query.get(store_id)
    form = GroceryStoreForm(obj=store)

    if form.validate_on_submit(): 
        form.populate_obj(store)
        db.session.add(store)
        db.session.commit()

        flash('Your store has been validated and updated. Thank you!')
        return redirect(url_for('main.store_detail', store_id = store))
    else: 
        store = GroceryStore.query.get(store_id)
        return render_template('store_detail.html', store=store)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
@login_required
def item_detail(item_id):
    item = GroceryItem.query.get(item_id)
    form = GroceryItemForm(obj=item)

    if form.validate_on_submit(): 
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()

        flash('Your item has been validated and updated. Thank you!')
        return redirect(url_for('main.item_detail', item_id = item))
    else: 
        item = GroceryItem.query.get(item_id)
        return render_template('item_detail.html', item=item)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    print('in signup')
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        print('created')
        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))

@main.route('/shopping_list')
@login_required
def shopping_list():
    shopping_list()
    return redirect(url_for('main.item_detail'))