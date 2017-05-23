from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, NumberRange

index_category = { 0:'actuator',
                     1:'cable',
                     2: 'controller',
                     3:'kit',
                     4:'misc',
                     5:'sensor',
                     6:'tool',
                     7:'wireless'}

category_index = { 'actuator':0,
                     'cable':1,
                     'controller':2,
                     'kit':3,
                     'misc':4,
                     'sensor':5,
                     'tool':6,
                     'wireless':7}

category_choices = [ (0,'actuator'),
                     (1,'cable'),
                     (2,'controller'),
                     (3,'kit'),
                     (4,'misc'),
                     (5,'sensor'),
                     (6,'tool'),
                     (7,'wireless')]

class EditPartForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message="Name required!")])
    description = TextAreaField('Description', validators=[DataRequired(message="Description Required!")])
    quantity = IntegerField('Quantity', validators=[NumberRange(min=0, max=1000, message='Quantity must be 0 or more!')])
    category = SelectField('Category', coerce=int, choices=category_choices)
    submit = SubmitField('Save Part')
