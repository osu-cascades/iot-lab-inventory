from iot_app import db, googlelogin
from flask_login import UserMixin

class Part(db.Model):
    __tablename__ = 'parts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(2048))
    category = db.Column(db.String(64))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String(256), primary_key=True, unique=True)
    name = db.Column(db.String(64))
    picture = db.Column(db.String(64))
    email = db.Column(db.String(64))

    def __init__(self,userinfo):
        self.id = userinfo['id']
        self.name = userinfo['name']
        self.picture = userinfo['picture']

@googlelogin.user_loader
def get_user(userid):
    return User.query.get(userid)


