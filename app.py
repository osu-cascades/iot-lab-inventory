import os
import dataset
import json
from flask import Flask, g, url_for, redirect, request, render_template, flash, session
from flask_login import UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.local import LocalProxy
from flask_googlelogin import GoogleLogin


app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(24)
app.config.update(
    #SECRET_KEY='Miengous3Xie5meiyae6iu6mohsaiRae',
    GOOGLE_LOGIN_CLIENT_ID='256102919201-qvjgcstktj5bimq3ffj8k5va85g0r137.apps.googleusercontent.com',
    GOOGLE_LOGIN_CLIENT_SECRET='X0HqD1zykF3i4Hvde2QsvkdL',
    GOOGLE_LOGIN_REDIRECT_URI='http://localhost:5000/oauth2callback')
googlelogin = GoogleLogin(app)

DATABASE_URL = 'sqlite:///data.sqlite'

# Helpers

def get_db():
    db = getattr(g, 'database', None)
    if db is None:
        db = g.database = dataset.connect(DATABASE_URL)
    return db


@app.teardown_appcontext
def teardown_db(exception):
    # NOOP. dataset API has no close() method.
    return

db = LocalProxy(get_db)


# Root

@app.route('/', methods=['GET'])
def home():
    parts = db['parts'].all()
    #return render_template('home.html', parts=parts)
    return render_template('home.html', parts=parts, user=current_user)

# Parts

@app.route('/parts', methods=['GET'])
def parts_list():
    category = request.args.get('category')
    if category is None:
        parts = db['parts'].all()
    else:
        parts = db['parts'].find(category=category)
    return render_template('parts/list.html', parts=parts)


@app.route('/parts/new', methods=['GET'])
def parts_new():
    return render_template('parts/new.html')


@app.route('/parts', methods=['POST'])
def parts_create():
    name = request.form['name']
    description = request.form['description']
    category = request.form['category']
    db.begin()
    try:
        db['parts'].insert(dict(name=name, description=description, category=category))
        db.commit()
        flash('Part added successfully.')
    except:
        flash('There was a problem adding this part.')
        db.rollback()
    return redirect(url_for('parts_list'))


@app.route('/parts/<int:id>/edit', methods=['GET'])
def parts_edit(id=id):
    part = db['parts'].find_one(id=id)
    return render_template('parts/edit.html', id=id, name=part['name'], description=part['description'], category=part['category'])


@app.route('/parts/<int:id>', methods=['POST'])
def parts_update(id):
    name = request.form['name']
    description = request.form['description']
    category = request.form['category']
    db.begin()
    try:
        db['parts'].update(dict(id=id, name=name, description=description, category=category), ['id'])
        db.commit()
        flash('Part ' + str(id) + ' updated.')
    except Exception as e:
        print(e)
        flash('There was a problem updating this part.')
        db.rollback()
    return redirect(url_for('parts_list'))


@app.route('/parts/<int:id>/delete', methods=['POST'])
def parts_delete(id):
    table = db['parts']
    table.delete(id=id)
    flash('Part ' + str(id) + ' has been deleted.')
    return redirect(url_for('parts_list'))

#logic for enabling Google Authentication

users = {}

class User(UserMixin):
    def __init__(self, userinfo):
        self.id = userinfo['id']
        self.name = userinfo['name']
        self.picture = userinfo.get('picture')


@googlelogin.user_loader
def get_user(userid):
    return users.get(userid)


@app.route('/login')
def login():
    #redirect user to log in with Google credentials
    return redirect(googlelogin.login_url(approval_prompt='force',scopes=['https://www.googleapis.com/auth/userinfo.email']))

@app.route('/profile')
@login_required
def profile():
    return """
        <p>Hello, %s</p>
        <p><img src="%s" width="100" height="100"></p>
        <p>Token: %r</p>
        <p>Extra: %r</p>
        <p><a href="/logout">Logout</a></p>
        """ % (current_user.name, current_user.picture, session.get('token'),session.get('extra'))


@app.route('/oauth2callback')
@googlelogin.oauth2callback
def login_oauth(token, userinfo, **params):
    user = users[userinfo['id']] = User(userinfo)
    login_user(user)
    session['token'] = json.dumps(token)
    session['extra'] = params.get('extra')
    #return redirect(params.get('next', url_for('.profile')))
    return redirect(params.get('next', url_for('.home')))

@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('home'))

#start the app
if __name__ == '__main__':
    app.run()
