from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_oauth2_login import GoogleLogin
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

google_login = GoogleLogin(app)
login_manager = LoginManager()
login_manager.init_app(app)

from .views.public import public
app.register_blueprint(public)

from .views.auth import auth
app.register_blueprint(auth)

from .views.users import users
app.register_blueprint(users)

from .views.admin import admin
app.register_blueprint(admin)

#error handling via blueprints is a known bug in flask
# abort(403) does not reach the blueprint route..
from .error_handlers import *
