from flask import Blueprint, url_for, redirect, request, render_template, flash, abort
from flask_login import login_required, login_user, current_user
from iot_lab_inventory import db
from iot_lab_inventory.models import User, Order, Part
from iot_lab_inventory.forms import EditPartForm, index_category, category_index
from functools import wraps

admin = Blueprint('admin', __name__)


# Admin

def admin_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return wrapped


@admin.route('/admin', methods=['GET'])
@login_required
@admin_required
def home():
    pending = Order.query.filter_by(status='Pending')
    reserved = Order.query.filter_by(status='Reserved')
    return render_template('admin/home.html', pending=pending, reserved=reserved)


# Users

@admin.route('/users', methods=['GET'])
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('users/list.html', users=users)


@admin.route('/users/<int:id>', methods=['POST'])
@login_required
@admin_required
def update_user(id):
    role = request.form.get('role')
    try:
        user = User.query.filter_by(id=id).first()
        if role == 'True':
            user.is_admin = True
        else:
            user.is_admin = False
        db.session.commit()
        flash('User updated.')
    except Exception as err:
        flash('Error: unable to update user role.')
    return redirect(url_for('admin.users'))


# Parts

@admin.route('/parts', methods=['POST'])
@login_required
@admin_required
def create_part():
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
            return redirect(url_for('public.parts'))
        except Exception as e:
            print(str(e))
            flash('There was a problem adding this part.')
            db.session.rollback()
    return render_template('parts/new.html', form=form)


@admin.route('/parts/new', methods=['GET'])
@login_required
@admin_required
def new_part(form=None):
    if form is None:
        form = EditPartForm()
    return render_template('parts/new.html', form=form)


@admin.route('/parts/<int:id>/edit', methods=['GET'])
@login_required
@admin_required
def edit_part(id=id):
    form = EditPartForm()
    part = Part.query.filter_by(id=id).first()
    form.name.data = part.name
    form.description.data = part.description
    form.quantity.data = part.inventory_item.quantity
    form.category.data = category_index[part.category]
    return render_template('parts/edit.html', part=part, form=form)


@admin.route('/parts/<int:id>', methods=['POST'])
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
    return redirect(url_for('public.parts'))


@admin.route('/parts/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def parts_delete(id):
    part = Part.query.filter_by(id=id).first()
    if part is not None:
        db.session.delete(part)
        db.session.commit()
        flash('Part ' + str(id) + ' has been deleted.')
    return redirect(url_for('public.parts'))


# Orders

@admin.route('/orders', methods=['GET'])
@login_required
@admin_required
def orders():
    orders = Order.query.all()
    return render_template('orders/list.html', orders=orders)


@admin.route('/orders/<int:id>/reserve', methods=['POST'])
@login_required
@admin_required
def orders_reserve(id):
    #send email to user
    order = Order.query.filter_by(id=id).first()
    order.status = "Reserved"
    return redirect(url_for('admin.home'))


@admin.route('/orders/<int:id>/rent', methods=['POST'])
@login_required
@admin_required
def orders_rent(id=id):
    #decrease numbers in inventory
    order = Order.query.filter_by(id=id).first()
    order.status = "Rented"
    return redirect(url_for('admin.home'))


@admin.route('/orders/<int:id>/update_status', methods=['POST'])
@login_required
@admin_required
def orders_update_status(id):
    order = Order.query.filter_by(id=id).first()
    return 'TODO'

#order: Pending => Reserved => Rented => Returned
