from iot_app import db
from flask_login import UserMixin

cart_parts = db.Table('cart_parts',
    db.Column('carts_id', db.Integer, db.ForeignKey('carts.id')),
    db.Column('parts_id', db.Integer, db.ForeignKey('parts.id'))
)

class Part(db.Model):
    __tablename__ = 'parts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(2048))
    category = db.Column(db.String(64))
    sparkfun_id = db.Column(db.String(64))
    images = db.relationship('Image', backref='part')
    documents = db.relationship('Document', backref='part')
    inventory_item = db.relationship('InventoryItem', back_populates='part', uselist=False, lazy='subquery')

class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, default=None, nullable=True)
    part_id = db.Column(db.Integer, db.ForeignKey('parts.id'))

class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, default=None, nullable=True)
    part_id = db.Column(db.Integer, db.ForeignKey('parts.id'))

class InventoryItem(db.Model):
    __tablename__ = 'inventory_items'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    part_id = db.Column(db.Integer, db.ForeignKey('parts.id'))
    part = db.relationship("Part", back_populates='inventory_item', uselist=False, lazy='subquery')

class CartItem():

    def __init__(self, inventory_item, quantity):
        self.inventory_item = inventory_item
        self.name = inventory_item.part.name
        self.quantity = quantity


class Cart():

    cart_items = []

    def add(self, cart_item):
        self.cart_items.append(cart_item)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String)
    name = db.Column(db.String)
    picture = db.Column(db.String)

    cart = Cart()

    # cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'))
    # cart = db.relationship('Cart', uselist=False, backref='user')

    def __init__(self, username, email, name, picture):
        self.username = username
        self.email = email
        self.name = name
        self.picture = picture




#save cart to session scope
#Order database table
#Rental database table
# order of ops
# - add part to cart
# - rent cart => send email to Marc / Yong
# - rental list "pending"
# - rental associated with inventory items (not parts)
# - admin checks out rental
# - changes status of inventory item to "rented"
# - update student's rental list
# - rental is date (request, needed, returned) inventory item, status, user

