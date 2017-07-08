from flask import Blueprint, url_for, redirect, request, render_template, flash, session, abort
from flask_login import login_required, current_user
from flask_mail import Message
from iot_lab_inventory import db, mail
from iot_lab_inventory.models import Part, Order, OrderItem

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
  cart = Order.query.filter_by(user=current_user, status='Cart').first()

  if cart is None:
    print 'creating new cart'
    cart = Order()
  return render_template('cart.html', cart=cart)


@users.route('/cart', methods=['POST'])
@login_required
def add_part_to_cart():
  part_id = int(request.form['part_id'])
  part = Part.query.filter_by(id=part_id).first()

  #get the Order with cart status
  cart = Order.query.filter_by(user=current_user, status='Cart').first()

  #if Order does not exist, create new Order
  if cart is None:
    print 'new cart'
    cart = Order()
    cart.status = 'Cart'
    cart.user = current_user

  # if order_item for part not in Order, create
  order_item = OrderItem.query.filter_by(order=cart, part=part).first()
  if order_item is None:
    order_item = OrderItem(part=part, order=cart, quantity=1)
    db.session.add(order_item)
    db.session.commit()
  # else, add 1 to order_item quantity
  else:
    order_item.quantity += 1

  return redirect(url_for('users.cart'))

@users.route('/cart/<int:id>/delete', methods=['POST'])
@login_required
def remove_part_from_cart(id):
  order_item = OrderItem.query.filter_by(id=id).first()
  db.session.delete(order_item)
  db.session.commit()
  return redirect(url_for('users.cart'))


@users.route('/cart/<int:id>/update', methods=['POST'])
@login_required
def update_part_in_cart(id):
  quantity = request.form.get('quantity')
  order_item = OrderItem.query.filter_by(id=id).first()
  order_item.quantity = int(quantity)
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
  cart = Order.query.filter_by(user=current_user, status='Cart').first()

  #check for empty cart
  if cart is None or len(cart.order_items) == 0:
    flash('No items in cart.')
    return redirect(url_for('users.cart'))

  #check inventory for quantity
  for order_item in cart.order_items:
    part = order_item.part
    if part.inventory_item.quantity < order_item.quantity:
      msg = 'Unable to create order: too few ' + part.name + ' in inventory.'
      flash(msg)
      return redirect(url_for('users.cart'))

  cart.status = 'Pending'

  # #send email to user saying order is pending..
  # msg = Message(subject='OSU-Cascades IoT-Lab: Order Pending ', \
  #               recipients=[ current_user.email ])
  # msg.body = render_template('mail/pending.txt', order=order)
  # msg.html = render_template('mail/pending.html', order=order)
  # mail.send(msg)

  return redirect(url_for('users.order', id=cart.id))
