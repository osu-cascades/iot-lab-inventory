from flask import Blueprint, url_for, redirect, request, render_template, flash, session, abort
from flask_login import login_required, current_user
from flask_mail import Message
from iot_lab_inventory import db, mail
from iot_lab_inventory.models import Part, CartItem, Order

users = Blueprint('users', __name__)

# Users

@users.route('/users/me', methods=['GET'])
@login_required
def home():
  return render_template('users/home.html')


# Cart

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
  current_user.cart.cart_items[id].quantity = int(quantity)
  return redirect(url_for('users.cart'))


# Order

@users.route('/orders/<int:id>', methods=['GET'])
@login_required
def order(id):
  order = Order.query.filter_by(id=id).first()
  if current_user.id != order.user_id and not current_user.is_admin:
    abort(403)
  return render_template('orders/order.html', order=order)


@users.route('/orders', methods=['POST'])
@login_required
def create_order():
  #check for empty cart
  if not current_user.cart.cart_items:
    flash('No items in cart.')
    return redirect(url_for('users.cart'))

  #check inventory for quantity
  for part_id in current_user.cart.cart_items:
    part = Part.query.filter_by(id=part_id).first()
    quantity = part.inventory_item.quantity
    cart_item = current_user.cart.cart_items[part_id]
    if cart_item.quantity > quantity:
      msg = 'Unable to create order: not enough ' + part.name + ' in inventory.'
      flash(msg)
      return redirect(url_for('users.cart'))

  order = Order(current_user.cart)
  db.session.add(order)
  db.session.commit()
  current_user.cart.cart_items.clear()

  #send email to user saying order is pending..
  msg = Message(subject='OSU-Cascades IoT-Lab: Order Pending ', \
                recipients=[ current_user.email ])
  msg.body = render_template('mail/pending.txt', order=order)
  msg.html = render_template('mail/pending.html', order=order)
  mail.send(msg)

  return redirect(url_for('users.order', id=order.id))
