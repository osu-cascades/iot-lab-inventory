from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_oauth2_login import GoogleLogin
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

google_login = GoogleLogin(app)
login_manager = LoginManager()
login_manager.init_app(app)

import iot_app.models
import iot_app.views
