from flask import Blueprint, url_for, redirect, request, render_template, flash, session, abort
from flask_login import login_user, current_user
from iot_lab_inventory import db, google_login
from iot_lab_inventory.models import Part, User

public = Blueprint('public', __name__)


@public.route('/', methods=['GET'])
def home():
    parts = Part.query.all()
    return render_template('home.html', parts=parts, user=current_user)


# Authentication

@public.route("/login")
def login():
    return redirect(google_login.authorization_url())


@google_login.login_success
def login_success(token, profile):
    if profile['hd'] != 'oregonstate.edu':
        flash('Log in failed. Did you use your OSU google account?')
        return redirect(url_for('public.home'))
    username = profile['email'].split('@')[0]
    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User(username, profile['email'], profile['name'], profile['picture'])
        db.session.add(user)
        db.session.commit()
    login_user(user)
    flash('You have successfully logged in.')
    return redirect(url_for('public.home'))


@google_login.login_failure
def login_failure(e):
    abort(401)


# Parts

@public.route('/parts', methods=['GET'])
def parts_list():
    category = request.args.get('category')
    if category is None:
        parts = Part.query.all()
    else:
        parts = Part.query.filter_by(category=category).all()
    return render_template('parts/list.html', parts=parts, category=category)


@public.route('/parts/<int:id>', methods=['GET'])
def part(id):
    part = Part.query.filter_by(id=id).first()
    return render_template('parts/part.html', part=part)

