from flask import render_template
from iot_lab_inventory import app

#known bug in flask: cannot put error handlers in blueprint
@app.errorhandler(401)
def unauthorized(e):
    return render_template('401.html'), 401

@app.errorhandler(403)
def unauthorized(e):
    return render_template('403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404