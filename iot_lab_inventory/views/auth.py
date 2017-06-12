from flask import Blueprint, url_for, redirect, flash, session, abort
from flask_login import login_user, logout_user, login_required
from iot_lab_inventory import db, google_login
from iot_lab_inventory.models import User

auth = Blueprint('auth', __name__)


@auth.route("/login")
def login():
    return redirect(google_login.authorization_url())


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('public.home'))


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

