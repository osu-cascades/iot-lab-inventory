import os

DEBUG=True
SECRET_KEY=os.urandom(24)
GOOGLE_LOGIN_CLIENT_ID = '256102919201-qvjgcstktj5bimq3ffj8k5va85g0r137.apps.googleusercontent.com'
GOOGLE_LOGIN_CLIENT_SECRET = 'X0HqD1zykF3i4Hvde2QsvkdL'
GOOGLE_LOGIN_REDIRECT_URI = 'http://localhost:5000/oauth2callback'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///data.sqlite'
