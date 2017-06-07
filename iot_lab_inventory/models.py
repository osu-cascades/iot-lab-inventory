from flask_login import UserMixin
from iot_lab_inventory import db, login_manager
from .cart import Cart, CartItem


orders_parts = db.Table('orders_parts', db.metadata,
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id')),
    db.Column('part_id', db.Integer, db.ForeignKey('parts.id'))
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
    inventory_item = db.relationship('InventoryItem', back_populates='part', uselist=False)
    orders = db.relationship("Order", secondary=orders_parts)


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


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    parts = db.relationship("Part", secondary=orders_parts)
    status = db.Column(db.String, default="Pending")
    created_at = db.Column(db.Date)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String)
    name = db.Column(db.String)
    picture = db.Column(db.String)
    is_admin = db.Column(db.Boolean)

    cart = Cart()

    def __init__(self, username, email, name, picture):
        self.username = username
        self.email = email
        self.name = name
        self.picture = picture
        self.is_admin = False

    @staticmethod
    @login_manager.user_loader
    def load_user(id):
        return User.query.filter_by(id=id).first()

