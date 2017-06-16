import os
import sys

if sys.version_info[0] < 3:
    SECRET_KEY = os.environ['FLASK_SECRET_KEY'].decode('string_escape')
else:
    SECRET_KEY = bytes(os.environ['FLASK_SECRET_KEY'], 'utf-8').decode('unicode_escape')

GOOGLE_LOGIN_CLIENT_ID = os.environ['GOOGLE_LOGIN_CLIENT_ID']
GOOGLE_LOGIN_CLIENT_SECRET = os.environ['GOOGLE_LOGIN_CLIENT_SECRET']
GOOGLE_LOGIN_REDIRECT_SCHEME = os.environ['GOOGLE_LOGIN_REDIRECT_SCHEME']

SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

S3_BUCKET_NAME = 'https://s3-us-west-2.amazonaws.com/osu-iot-lab-inventory/'

# MAIL_SERVER='smtp.gmail.com'
# MAIL_PORT = 465
# MAIL_USERNAME = os.environ['GMAIL_ADDRESS']
# MAIL_DEFAULT_SENDER = os.environ['GMAIL_ADDRESS']
# MAIL_PASSWORD = os.environ['GMAIL_PASSWORD']
# MAIL_USE_TLS = False
# MAIL_USE_SSL = True
# MAIL_SUPPRESS_SEND=True