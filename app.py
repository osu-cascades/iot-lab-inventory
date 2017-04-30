from flask import Flask, url_for, redirect, request
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
            db['parts'].insert(dict(name=name,desc=desc, type=type))
            db.commit()
        except:
            db.rollback()

        print name + ": " + desc + ", " + type
        return redirect(url_for('retrieve'))

    return app.send_static_file('create.html')

#get all records from database
@app.route('/retrieve.html')
def retrieve():
    retval = '<h1>Parts:</h1>'
    retval += '<ul>'
    # connect to database, make transaction
    db = dataset.connect('sqlite:///data.sqlite')
    parts = db['parts'].all()
    for part in parts:
        retval += '<li>' + part['name'] + ": " + part['desc'] + ', (' + part['type'] + ')</li>'

    retval += '</ul>'
    return retval

#this must come at the end (to allow decorators to be set)
if __name__ == "__main__":
    app.run()