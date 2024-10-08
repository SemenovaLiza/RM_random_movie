from flask import render_template

from . import app, db


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error_pages/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollabck()
    return render_template('error_pages/500.html'), 500
