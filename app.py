from flask import Flask, url_for, redirect, request, render_template
import os
import dataset
app = Flask(__name__)

#app.debug allows error messages and on the fly code changes
app.debug=True
app.secret_key = os.urandom(24)

# #this serves static pages
@app.route('/<path:path>')
def get_static(path):
    return app.send_static_file(path)

@app.route('/', methods=['GET','POST'])
@app.route('/index.html',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        name = request.form['username']
        return '<h1>Welcome ' + name + '!</h1>'

    else:
        return app.send_static_file('index.html')

#route to create a new part
@app.route('/create.html', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['desc']
        type = request.form['type']

        # connect to database, make transaction
        db = dataset.connect('sqlite:///data.sqlite')
        db.begin()
        try:
            db['parts'].insert(dict(name=name, desc=desc, type=type))
            db.commit()
        except:
            db.rollback()

        print name + ": " + desc + ", " + type
        return redirect(url_for('retrieve'))

    else:
        return app.send_static_file('create.html')

#get all records from database
@app.route('/retrieve')
@app.route('/retrieve.html')
def retrieve():
    retval = '<h1>Parts:</h1>'
    retval += '<ul>'
    # connect to database, make transaction
    db = dataset.connect('sqlite:///data.sqlite')
    parts = db['parts'].all()
    for part in parts:
        retval += '<li>'
        for k in part.keys():
            retval += str(k) + ": " + str(part[k]) + ", "

        retval += '<a href="update/' + str(part['id']) + '"> Update</a>'
        retval += ', <a href="delete/' + str(part['id']) + '"> Delete</a>'
        retval += "</li>"

    retval += '</ul>'
    return retval

@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):

    if request.method=='GET':
        db = dataset.connect('sqlite:///data.sqlite')
        part = db['parts'].find_one(id=id)
        return render_template('update.html', id=id, name=part['name'], desc=part['desc'], type=part['type'] )
    elif request.method=='POST':
        name = request.form['name']
        desc = request.form['desc']
        type = request.form['type']

        # connect to database, make transaction
        db = dataset.connect('sqlite:///data.sqlite')
        db.begin()
        try:
            db['parts'].update(dict(id=id, name=name, desc=desc, type=type),['id'])
            db.commit()
        except Exception as e:
            print e
            db.rollback()

        print name + ": " + desc + ", " + type
        return redirect(url_for('retrieve'))

@app.route('/delete/<id>')
def delete(id):
    db = dataset.connect('sqlite:///data.sqlite')
    table = db['parts']
    table.delete(id=id)
    return '<h1> TODO: deleted part #: ' + id + '<h1>'

#this must come at the end (to allow decorators to be set)
if __name__ == "__main__":
    app.run()
