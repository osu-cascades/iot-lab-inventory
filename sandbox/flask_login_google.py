import os

from flask import Flask, jsonify, redirect, url_for
from flask_oauth2_login import GoogleLogin
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.update(
    SECRET_KEY="secret",
    GOOGLE_LOGIN_REDIRECT_SCHEME="http",
)

app.config['GOOGLE_LOGIN_CLIENT_ID']= os.environ['GOOGLE_LOGIN_CLIENT_ID']
app.config['GOOGLE_LOGIN_CLIENT_SECRET'] = os.environ['GOOGLE_LOGIN_CLIENT_SECRET']
google_login = GoogleLogin(app)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_user.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String)
    name = db.Column(db.String)
    picture = db.Column(db.String)

    def __init__(self, username, email, name, picture):
        self.username = username
        self.email = email
        self.name = name
        self.picture = picture

# class User(UserMixin):
#     # proxy for a database of users
#     user_database = {"JohnDoe": ("JohnDoe", "John"),
#                "JaneDoe": ("JaneDoe", "Jane")}
#
#     def __init__(self, username, password):
#         self.id = username
#         self.password = password
#
#     @classmethod
#     def get(cls,id):
#         return cls.user_database.get(id)


@login_manager.user_loader
def load_user(id):
    print 'requesting user with id =',id
    user = User.query.filter_by(id=id).first()
    if user is not None:
        return user
    else:
        return None

@app.route("/")
def index():
    return '''
        <a href="%s">Login</a><br>
    ''' % (url_for('login'))

@app.route("/login")
def login():
    return redirect(google_login.authorization_url())

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/private')
@login_required
def private_url():
    return '''
        <a href="%s">Logout</a><br>
        hello: %s<br>
        <img height="100" src="%s"/>
    ''' % (url_for('logout'), current_user.name, current_user.picture)

@google_login.login_success
def login_success(token, profile):
    username = profile['email'].split('@')[0]

    #check to see if user in db
    user = User.query.filter_by(username=username).first()
    if user is None: #if not, create new user
        email = profile['email']
        name = profile['name']
        picture = profile['picture']
        user = User(username, email, name, picture)
        db.session.add(user)
        db.session.commit()

    login_user(user)
    return 'LOGIN OK'

@google_login.login_failure
def login_failure(e):
    return jsonify(error=str(e))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)


#TODO:
# integrate with app