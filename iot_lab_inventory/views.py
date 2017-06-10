from flask import url_for, redirect, request, render_template, flash, session, abort
from flask_login import login_required, login_user, current_user, logout_user
from iot_lab_inventory import app, db, google_login
from .models import Part, User, InventoryItem, CartItem, Cart, Order
from .forms import EditPartForm, index_category, category_index
from functools import wraps


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
    abort(401)
    # return jsonify(error=str(e))


# Users

@app.route('/users/me')
@login_required
def users_current_user():
    return render_template('users/current_user.html')


# Admin

def admin_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return wrapped


@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    pending = Order.query.filter_by(status='Pending')
    reserved = Order.query.filter_by(status='Reserved')
    return render_template('admin/dashboard.html', pending=pending, reserved=reserved)


@app.route('/admin/manage_users')
@login_required
@admin_required
def admin_manage_users():
    users = User.query.all()
    return render_template('admin/manage_users.html', users=users)


@app.route('/admin/manage_users', methods=['POST'])
@login_required
@admin_required
def admin_update_user_role():
    user_id = int(request.form['user_id'])
    role = request.form.get('role')

    try:
        user = User.query.filter_by(id=user_id).first()
        if role == 'True':
            user.is_admin = True
        else:
            user.is_admin = False
        db.session.commit()
        flash('Updated user role')

    except Exception as err:
        flash('ERROR: unable to update user role')

    return redirect(url_for('admin_manage_users'))


@app.route('/admin/manage_orders')
@login_required
@admin_required
def admin_manage_orders():
    orders = Order.query.all()
    return render_template('admin/manage_orders.html', orders=orders)


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
@admin_required
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
@admin_required
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
@admin_required
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
@admin_required
def parts_delete(id):
    part = Part.query.filter_by(id=id).first()
    if part is not None:
        db.session.delete(part)
        db.session.commit()
        flash('Part ' + str(id) + ' has been deleted.')
    return redirect(url_for('parts_list'))


# Carts

@app.route('/cart', methods=['GET'])
@login_required
def cart():
    return render_template('cart.html')


@app.route('/cart', methods=['POST'])
@login_required
def add_part_to_cart():
    part_id = int(request.form['part_id'])
    if part_id in current_user.cart.cart_items:
        current_user.cart.cart_items[part_id].quantity += 1
    else:
        part = Part.query.filter_by(id=part_id).first()
        cart_item = CartItem(part.inventory_item, 1)
        current_user.cart.add(part_id, cart_item)
    return redirect(url_for('cart'))


@app.route('/cart/<int:id>/delete', methods=['POST'])
@login_required
def remove_part_from_cart(id):
    current_user.cart.cart_items.pop(int(request.form['id']))
    return redirect(url_for('cart'))


# Orders

@app.route('/orders/<int:id>')
@login_required
def orders_view(id):
    order = Order.query.filter_by(id=id).first()
    return render_template('orders/order.html', order=order)


@app.route('/orders', methods=['POST'])
@login_required
def orders_create():
    order = Order(current_user.cart)
    db.session.add(order)
    db.session.commit()
    current_user.cart.cart_items.clear()
    return redirect(url_for('orders_view', id=order.id))


@app.route('/orders/<int:id>/reserve', methods=['POST'])
@login_required
@admin_required
def orders_reserve(id):
    #send email to user
    order = Order.query.filter_by(id=id).first()
    order.status = "Reserved"
    return redirect(url_for('admin_dashboard'))



@app.route('/orders/<int:id>/rent', methods=['POST'])
@login_required
@admin_required
def orders_rent(id=id):
    #decrease numbers in inventory
    order = Order.query.filter_by(id=id).first()
    order.status = "Rented"
    return redirect(url_for('admin_dashboard'))


@app.route('/orders/<int:id>/update_status', methods=['POST'])
@login_required
@admin_required
def orders_update_status(id):
    order = Order.query.filter_by(id=id).first()
    return 'TODO'

#order: Pending => Reserved => Rented => Returned

# Errors

@app.errorhandler(401)
def unauthorized(e):
    return render_template('401.html'), 401


@app.errorhandler(403)
def unauthorized(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

