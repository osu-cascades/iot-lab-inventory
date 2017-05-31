from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

parts = db.Table('parts',
    db.Column('cart_id', db.Integer, db.ForeignKey('cart.id')),
    db.Column('part_id', db.Integer, db.ForeignKey('part.id'))
)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parts = db.relationship('Part', secondary=parts, backref=db.backref('carts', lazy='dynamic'))

class Part(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    cart = db.relationship('Cart', uselist=False, backref='user')

    def __init__(self, name):
        self.name = name

#main()
if __name__ == '__main__':

    db.drop_all()
    db.create_all()

    cart1 = Cart()
    cart2 = Cart()

    part1 = Part('p1')
    part2 = Part('p2')
    part3 = Part('p3')

    cart1.parts = [part1, part3]
    cart2.parts = [part1, part2, part3]

    db.session.add(cart1)
    db.session.add(cart2)
    db.session.commit()

    cart = Cart.query.filter_by(id=1).first()
    for p in cart.parts:
        print(cart.id, p.name)

    cart = Cart.query.filter_by(id=2).first()
    for p in cart.parts:
        print(cart.id, p.name)


    user1 = User('Marc')
    print(user1.name)
    user1.cart = Cart()
    user1.cart.parts = [part1, part3]
    for p in user1.cart.parts:
        print(p.name)



