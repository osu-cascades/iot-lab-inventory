from flask import Blueprint, url_for, redirect, request, render_template, flash, session, abort
from flask_login import login_required, login_user, current_user, logout_user
from iot_lab_inventory import db, google_login
from iot_lab_inventory.models import Part, User, InventoryItem, CartItem, Cart, Order

public = Blueprint('public', __name__)


@public.route('/', methods=['GET'])
def home():
    parts = Part.query.all()
    return render_template('home.html', parts=parts, user=current_user)


# Authentication

@public.route("/login")
def login():
    return redirect(google_login.authorization_url())


@public.route('/logout')
def logout():
    logout_user()
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
    # return jsonify(error=str(e))


# Users

@public.route('/users/me')
@login_required
def users_current_user():
    return render_template('users/current_user.html')


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


# Carts

@public.route('/cart', methods=['GET'])
@login_required
def cart():
    return render_template('cart.html')


@public.route('/cart', methods=['POST'])
@login_required
def add_part_to_cart():
    part_id = int(request.form['part_id'])
    if part_id in current_user.cart.cart_items:
        current_user.cart.cart_items[part_id].quantity += 1
    else:
        part = Part.query.filter_by(id=part_id).first()
        cart_item = CartItem(part.inventory_item, 1)
        current_user.cart.add(part_id, cart_item)
    return redirect(url_for('public.cart'))


@public.route('/cart/<int:id>/delete', methods=['POST'])
@login_required
def remove_part_from_cart(id):
    current_user.cart.cart_items.pop(id)
    return redirect(url_for('public.cart'))


@public.route('/cart/<int:id>/update', methods=['POST'])
@login_required
def update_part_in_cart(id):
    quantity = request.form.get('quantity')
    current_user.cart.cart_items[id].quantity = quantity
    return redirect(url_for('public.cart'))


# Orders

@public.route('/orders/<int:id>')
@login_required
def orders_view(id):
    order = Order.query.filter_by(id=id).first()
    return render_template('orders/order.html', order=order)


@public.route('/orders', methods=['POST'])
@login_required
def orders_create():
    order = Order(current_user.cart)
    db.session.add(order)
    db.session.commit()
    current_user.cart.cart_items.clear()
    return redirect(url_for('public.orders_view', id=order.id))


# Errors

@public.errorhandler(401)
def unauthorized(e):
    return render_template('401.html'), 401


@public.errorhandler(403)
def unauthorized(e):
    return render_template('403.html'), 403


@public.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

