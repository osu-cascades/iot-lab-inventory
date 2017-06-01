from flask_login import UserMixin
from iot_app import db, login_manager


class Part(db.Model):
    __tablename__ = 'parts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(2048))
    category = db.Column(db.String(64))
    sparkfun_id = db.Column(db.String(64))
    images = db.relationship('Image', backref='part')
    documents = db.relationship('Document', backref='part')
    inventory_item = db.relationship('InventoryItem', back_populates='part', uselist=False)


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
    part = db.relationship("Part", back_populates='inventory_item', uselist=False)


class CartItem():

    def __init__(self, inventory_item, quantity):
        self.inventory_item = inventory_item
        self.name = inventory_item.part.name
        self.quantity = quantity

        try:
            self.image = inventory_item.part.images[0].filename
        except Exception as e:
            self.image = None

class Cart():

    cart_items = {}

    def add(self, id, cart_item):
        self.cart_items[id] = cart_item


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String)
    name = db.Column(db.String)
    picture = db.Column(db.String)

    cart = Cart()

    def __init__(self, username, email, name, picture):
        self.username = username
        self.email = email
        self.name = name
        self.picture = picture

    @staticmethod
    @login_manager.user_loader
    def load_user(id):
        user = User.query.filter_by(id=id).first()
        if user is not None:
            return user
        else:
            return None
