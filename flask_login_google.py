import os

from flask import Flask, jsonify, redirect, url_for
from flask_oauth2_login import GoogleLogin
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user, logout_user

app = Flask(__name__)
app.config.update(
    SECRET_KEY="secret",
    GOOGLE_LOGIN_REDIRECT_SCHEME="http",
)

app.config['GOOGLE_LOGIN_CLIENT_ID']= ''
app.config['GOOGLE_LOGIN_CLIENT_SECRET'] = ''

google_login = GoogleLogin(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    # proxy for a database of users
    user_database = {"JohnDoe": ("JohnDoe", "John"),
               "JaneDoe": ("JaneDoe", "Jane")}

    def __init__(self, username, password):
        self.id = username
        self.password = password

    @classmethod
    def get(cls,id):
        return cls.user_database.get(id)

@login_manager.user_loader
def load_user(id):
    print 'load_user ', id
    user = User.get('plark')
    if user is not None:
        return User(user[0], user[1])
    return None

@app.route("/")
def index():
    return """
<html>
<a href="{}">Login with Google</a>
""".format(google_login.authorization_url())

@app.route("/login")
def login():
    print google_login.authorization_url()
    return redirect(google_login.authorization_url())

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/private')
@login_required
def private_url():
    return 'hello'

@google_login.login_success
def login_success(token, profile):
    print profile['family_name'], profile['email'], profile['hd']
    user = User(username='plark', password='cat')
    User.user_database[user.id] = (user.id, user.password)
    login_user(user)
    return jsonify(token=token, profile=profile)

@google_login.login_failure
def login_failure(e):
    return jsonify(error=str(e))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)


#TODO:
# create User database
# store profile info from google
# integrate with app