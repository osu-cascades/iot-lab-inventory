from flask import url_for, redirect, request, render_template, flash, session
from flask_login import login_required, login_user, current_user, logout_user
from iot_lab_inventory import app, db, google_login
from .models import Part, User, InventoryItem, CartItem, Cart
from .forms import EditPartForm, index_category, category_index


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/', methods=['GET'])
def home():
    parts = Part.query.all()
    return render_template('home.html', parts=parts, user=current_user)


# Authentication

@app.route("/login")
def login():
    return redirect(google_login.authorization_url())


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@google_login.login_success
def login_success(token, profile):
    if profile['hd'] != 'oregonstate.edu':
        flash('Log in failed. Did you use your OSU google account?')
        return redirect(url_for('home'))
    username = profile['email'].split('@')[0]
    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User(username, profile['email'], profile['name'], profile['picture'])
        db.session.add(user)
        db.session.commit()
    login_user(user)
    flash('You have successfully logged in.')
    return redirect(url_for('home'))


@google_login.login_failure
def login_failure(e):
    return jsonify(error=str(e))


# Users

@app.route('/users/me')
def users_current_user():
    return render_template('users/current_user.html')


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
@login_required
def parts_new(form=None):
    if form is None:
        form = EditPartForm()
    return render_template('parts/new.html',form=form)


@app.route('/parts/<int:id>', methods=['GET'])
def part(id):
    part = Part.query.filter_by(id=id).first()
    return render_template('parts/part.html', part=part)


@app.route('/parts', methods=['POST'])
@login_required
def parts_create():
    form = EditPartForm(request.form)
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        category = index_category[form.category.data]
        quantity = form.quantity.data
        try:
            inventory_item = InventoryItem(quantity=quantity)
            part = Part(name=name, description=description, category=category, inventory_item=inventory_item)
            db.session.add(part)
            db.session.commit()
            flash('Part added successfully.')
            return redirect(url_for('parts_list'))
        except Exception as e:
            flash('There was a problem adding this part.')
            db.session.rollback()
    return render_template('parts/new.html', form=form)


@app.route('/parts/<int:id>/edit', methods=['GET'])
@login_required
def parts_edit(id=id):
    form = EditPartForm()
    part = Part.query.filter_by(id=id).first()
    form.name.data = part.name
    form.description.data = part.description
    form.quantity.data = part.inventory_item.quantity
    form.category.data = category_index[part.category]
    return render_template('parts/edit.html', part=part, form=form)


@app.route('/parts/<int:id>', methods=['POST'])
@login_required
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
            print(e)
            flash('There was a problem updating this part.')
            db.session.rollback()
    else:
        part = Part.query.filter_by(id=id).first()
        return render_template('parts/edit.html', part=part, form=form)
    return redirect(url_for('parts_list'))


@app.route('/parts/<int:id>/delete', methods=['POST'])
@login_required
def parts_delete(id):
    part = Part.query.filter_by(id=id).first()
    if part is not None:
        db.session.delete(part)
        db.session.commit()
        flash('Part ' + str(id) + ' has been deleted.')
    return redirect(url_for('parts_list'))


@app.route('/parts/<int:id>/add_to_cart')
@login_required
def parts_add_to_cart(id):
    if id in current_user.cart.cart_items:
        current_user.cart.cart_items[id].quantity += 1
    else:
        part = Part.query.filter_by(id=id).first()
        cart_item = CartItem(part.inventory_item, 1)
        current_user.cart.add(id,cart_item)
    return redirect(url_for('view_cart'))


# Carts

@app.route('/cart')
@login_required
def view_cart():
    return render_template('cart.html')


@app.route('/cart/remove_from_cart/<int:id>')
@login_required
def remove_from_cart(id):
    print(id)
    current_user.cart.cart_items.pop(id)
    return redirect(url_for('view_cart'))

