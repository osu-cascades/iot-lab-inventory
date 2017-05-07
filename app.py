from flask import Flask, g, url_for, redirect, request, render_template, flash
# from flask_googlelogin import GoogleLogin
from werkzeug.local import LocalProxy
import os
import dataset


app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(24)
# googleLogin = GoogleLogin(app)

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


# Static files

@app.route('/<path:path>')
def get_static(path):
    return app.send_static_file(path)


# Root

@app.route('/', methods=['GET'])
def index():
    parts = db['parts'].all()
    return render_template("home.html", parts=parts)


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

# #Google Login auth stuffs
# @app.route('/oauth2callback')
# @googlelogin.oauth2callback
# def create_or_update_user(token, userinfo, **params):
#     user = User.filter_by(google_id=userinfo['id']).first()
#     if user:
#         user.name = userinfo['name']
#         user.avatar = userinfo['picture']
#     else:
#         user = User(google_id=userinfo['id'],
#                     name=userinfo['name'],
#                     avatar=userinfo['picture'])
#     db.session.add(user)
#     db.session.flush()
#     login_user(user)
#     return redirect(url_for('index'))
