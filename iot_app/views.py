from iot_app import app
import json
from flask import url_for, redirect, request, render_template, flash, session
from flask_login import login_required, login_user, logout_user, current_user
from iot_app import db, googlelogin
from models import Part, User

@app.route('/', methods=['GET'])
def home():
    parts = Part.query.all()
    return render_template('home.html', parts=parts, user=current_user)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Parts

@app.route('/parts', methods=['GET'])
def parts_list():
    category = request.args.get('category')
    if category is None:
        parts = Part.query.all()
    else:
        parts = Part.query.filter_by(category=category).all()
    return render_template('parts/list.html', parts=parts)


@app.route('/parts/new', methods=['GET'])
# @login_required
def parts_new():
    return render_template('parts/new.html')

@app.route('/parts', methods=['POST'])
def parts_create():
    name = request.form['name']
    description = request.form['description']
    category = request.form['category']
    try:
        part = Part(name=name, description=description, category=category)
        db.session.add(part)
        db.session.commit()
        flash('Part added successfully.')
    except:
        flash('There was a problem adding this part.')
        #db.rollback()
    return redirect(url_for('parts_list'))


@app.route('/parts/<int:id>/edit', methods=['GET'])
def parts_edit(id=id):
    part = Part.query.filter_by(id=id).first()
    return render_template('parts/edit.html', id=id, name=part.name, description=part.description,category=part.category)

@app.route('/parts/<int:id>', methods=['POST'])
def parts_update(id):
    name = request.form['name']
    description = request.form['description']
    category = request.form['category']
    try:
        part = Part.query.filter_by(id=id).first()
        part.name = name
        part.description = description
        part.category = category
        db.session.commit()
        flash('Part ' + str(id) + ' updated.')
    except Exception as e:
        print(e)
        flash('There was a problem updating this part.')
        # db.rollback()
    return redirect(url_for('parts_list'))


@app.route('/parts/<int:id>/delete', methods=['POST'])
def parts_delete(id):
    part = Part.query.filter_by(id=id).first()
    if part is not None:
        db.session.delete(part)
        db.session.commit()
        flash('Part ' + str(id) + ' has been deleted.')
    return redirect(url_for('parts_list'))

@app.route('/login')
def login():
    return redirect(googlelogin.login_url(approval_prompt='force',scopes=['https://www.googleapis.com/auth/userinfo.email']))

@app.route('/user')
@login_required
def user():
    return render_template('user.html')

@app.route('/oauth2callback')
@googlelogin.oauth2callback
def login_oauth(token, userinfo, **params):
    user = User.query.filter_by(id=userinfo['id']).first()
    if user is None:
        user = User(userinfo)
        db.session.add(user)
        db.session.commit()
    login_user(user)
    session['token'] = json.dumps(token)
    session['extra'] = params.get('extra')
    return redirect(params.get('next', url_for('.home')))

@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('home'))
