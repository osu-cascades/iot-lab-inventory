from flask import Blueprint, url_for, redirect, request, render_template, flash, session
from flask_login import login_required, current_user, logout_user
from iot_lab_inventory import db
from iot_lab_inventory.models import Part, CartItem, Order

users = Blueprint('users', __name__)


# Authentication

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.home'))


# Users

@users.route('/users/me')
@login_required
def users_current_user():
    return render_template('users/current_user.html')


# Carts

@users.route('/cart', methods=['GET'])
@login_required
def cart():
    return render_template('cart.html')


@users.route('/cart', methods=['POST'])
@login_required
def add_part_to_cart():
    part_id = int(request.form['part_id'])
    if part_id in current_user.cart.cart_items:
        current_user.cart.cart_items[part_id].quantity += 1
    else:
        part = Part.query.filter_by(id=part_id).first()
        cart_item = CartItem(part.inventory_item, 1)
        current_user.cart.add(part_id, cart_item)
    return redirect(url_for('users.cart'))


@users.route('/cart/<int:id>/delete', methods=['POST'])
@login_required
def remove_part_from_cart(id):
    current_user.cart.cart_items.pop(id)
    return redirect(url_for('users.cart'))


@users.route('/cart/<int:id>/update', methods=['POST'])
@login_required
def update_part_in_cart(id):
    quantity = request.form.get('quantity')
    current_user.cart.cart_items[id].quantity = quantity
    return redirect(url_for('users.cart'))


# Orders

@users.route('/orders/<int:id>')
@login_required
def orders_view(id):
    order = Order.query.filter_by(id=id).first()
    return render_template('orders/order.html', order=order)


@users.route('/orders', methods=['POST'])
@login_required
def orders_create():
    order = Order(current_user.cart)
    db.session.add(order)
    db.session.commit()
    current_user.cart.cart_items.clear()
    return redirect(url_for('users.orders_view', id=order.id))
