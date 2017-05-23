from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_googlelogin import GoogleLogin
from flask_migrate import Migrate
# from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object('config')
googlelogin = GoogleLogin(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
# Bootstrap(app)


@app.errorhandler(404)
def page_not_found(e):
    return '<h1>Not Found</h1>',404

import iot_app.models
import iot_app.views

