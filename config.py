import os

DEBUG=True
SECRET_KEY=os.urandom(24)
GOOGLE_LOGIN_CLIENT_ID = os.environ['GOOGLE_LOGIN_CLIENT_ID']
GOOGLE_LOGIN_CLIENT_SECRET = os.environ['GOOGLE_LOGIN_CLIENT_SECRET']
GOOGLE_LOGIN_REDIRECT_SCHEME = 'http'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "sqlite:///{0}/data.sqlite".format(os.path.join(os.path.abspath(os.path.dirname(__file__))))
