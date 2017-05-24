from iot_app import app
import json
from flask import url_for, redirect, request, render_template, flash, session
from flask_login import login_required, login_user, logout_user, current_user
from iot_app import db, googlelogin
from models import Part, User, InventoryItem
from forms import EditPartForm, index_category, category_index

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
    return render_template('parts/list.html', parts=parts, category=category)


@app.route('/parts/new', methods=['GET'])
# @login_required
def parts_new(form=None):
    if form is None:
        form = EditPartForm()
    return render_template('parts/new.html',form=form)

@app.route('/parts/<int:id>/detail')
def parts_detail(id):
    part = Part.query.filter_by(id=id).first()
    return render_template('parts/detail.html', part=part)

@app.route('/parts', methods=['POST'])
def parts_create():
    form = EditPartForm(request.form)

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        category = index_category[form.category.data]
        quantity = form.quantity.data
        try:
            inventory_item = InventoryItem(quantity=quantity)
            part = Part(name=name,description=description,category=category,inventory_item=inventory_item)
            db.session.add(part)
            db.session.commit()
            flash('Part added successfully.')
            return redirect(url_for('parts_list'))
        except Exception as e:
            flash('There was a problem adding this part.')
            db.session.rollback()
    return render_template('parts/new.html', form=form)

#using WTF forms
@app.route('/parts/<int:id>/edit', methods=['GET'])
def parts_edit(id=id):
    form = EditPartForm()
    part = Part.query.filter_by(id=id).first()
    form.name.data = part.name
    form.description.data = part.description
    form.quantity.data = part.inventory_item.quantity
    form.category.data = category_index[part.category]
    return render_template('parts/edit.html', part=part, form=form)

@app.route('/parts/<int:id>', methods=['POST'])
def parts_update(id):
    form = EditPartForm(request.form)
    if form.validate_on_submit():
        try:
            part = Part.query.filter_by(id=id).first()
            part.name = form.name.data
            part.description = form.description.data
            part.category = index_category[form.category.data]
            part.inventory_item.quantity = form.quantity.data
            db.session.commit()
            flash('Part ' + str(id) + ' updated.')
        except Exception as e:
            print e
            flash('There was a problem updating this part.')
            db.session.rollback()
    else:
        part = Part.query.filter_by(id=id).first()
        return render_template('parts/edit.html', part=part, form=form)

    return redirect(url_for('parts_list'))


@app.route('/parts/<int:id>/delete', methods=['POST'])
def parts_delete(id):
    part = Part.query.filter_by(id=id).first()
    if part is not None:
        db.session.delete(part)
        db.session.commit()
        flash('Part ' + str(id) + ' has been deleted.')
    return redirect(url_for('parts_list'))

@app.route('/parts/<int:id>/add_to_cart')
def parts_add_to_cart(id):
    part = Part.query.filter_by(id=id).first()
    return '<h1>Adding ' + part.name + ' to cart... </h1>'


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

