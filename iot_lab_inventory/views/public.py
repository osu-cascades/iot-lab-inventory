from flask import Blueprint, request, render_template
from flask_login import current_user
from iot_lab_inventory.models import Part

public = Blueprint('public', __name__)


@public.route('/', methods=['GET'])
def home():
    parts = Part.query.all()
    return render_template('home.html', parts=parts)


@public.route('/parts', methods=['GET'])
def parts():
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

