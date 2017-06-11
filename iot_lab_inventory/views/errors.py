from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.errorhandler(401)
def unauthorized(e):
    return render_template('401.html'), 401


@errors.errorhandler(403)
def unauthorized(e):
    return render_template('403.html'), 403


@errors.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
