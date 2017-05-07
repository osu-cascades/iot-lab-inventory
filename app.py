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

@app.route('/parts')
def retrieve():
    db = dataset.connect(DATABASE_URL)
    category = request.args.get('category')
    if category is None:
        parts = db['parts'].all()
    else:
        parts = db['parts'].find(type=category)
    return render_template("retrieve.html", parts=parts)

@app.route('/create.html', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['desc']
        type = request.form['type']

        db = dataset.connect(DATABASE_URL)
        db.begin()
        try:
            db['parts'].insert(dict(name=name, desc=desc, type=type))
            db.commit()
        except:
            db.rollback()

        return redirect(url_for('retrieve'))

    else:
        return render_template('create.html')

@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    if request.method=='GET':
        db = dataset.connect(DATABASE_URL)
        part = db['parts'].find_one(id=id)
        return render_template('update.html', id=id, name=part['name'], desc=part['desc'], type=part['type'] )
    elif request.method=='POST':
        name = request.form['name']
        desc = request.form['desc']
        type = request.form['type']
        db = dataset.connect(DATABASE_URL)
        db.begin()
        try:
            db['parts'].update(dict(id=id, name=name, desc=desc, type=type),['id'])
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()

        return redirect(url_for('retrieve'))

@app.route('/delete/<id>')
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
