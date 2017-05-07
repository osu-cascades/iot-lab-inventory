from flask import Flask, url_for, redirect, request, render_template
# from flask_googlelogin import GoogleLogin
import os
import dataset


app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(24)
# googleLogin = GoogleLogin(app)

DATABASE_URL = 'sqlite:///data.sqlite'


# Static files

@app.route('/<path:path>')
def get_static(path):
    return app.send_static_file(path)


# Root

@app.route('/', methods=['GET'])
def index():
    db = dataset.connect(DATABASE_URL)
    parts = db['parts'].all()
    return render_template("home.html", parts=parts)


# Parts

@app.route('/parts', methods=['GET'])
def parts_list():
    db = dataset.connect(DATABASE_URL)
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
    db = dataset.connect(DATABASE_URL)
    db.begin()
    try:
        db['parts'].insert(dict(name=name, description=description, category=category))
        db.commit()
    except:
        db.rollback()
    return redirect(url_for('parts_list'))


@app.route('/parts/edit/<int:id>', methods=['GET'])
def parts_edit(id=id):
    db = dataset.connect(DATABASE_URL)
    part = db['parts'].find_one(id=id)
    return render_template('parts/edit.html', id=id, name=part['name'], description=part['description'], category=part['category'])


@app.route('/parts/<int:id>', methods=['POST'])
def update(id):
    name = request.form['name']
    description = request.form['description']
    category = request.form['category']
    db = dataset.connect(DATABASE_URL)
    db.begin()
    try:
        db['parts'].update(dict(id=id, name=name, description=description, category=category), ['id'])
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
    return redirect(url_for('parts_list'))


@app.route('/delete/<int:id>')
def delete(id):
    db = dataset.connect(DATABASE_URL)
    table = db['parts']
    table.delete(id=id)
    return '<h1> TODO: deleted part #: ' + id + '<h1>'

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
