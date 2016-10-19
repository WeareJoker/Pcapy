import os

from flask import send_file
from flask import send_from_directory

from app.config import PROJECT_ROOT
from app import app


@app.route('/css/<path:filename>')
def css_static(filename):
    return send_from_directory(os.path.join(PROJECT_ROOT, 'static/css/'), filename)


@app.route('/js/<path:filename>')
def js_static(filename):
    return send_from_directory(os.path.join(PROJECT_ROOT, 'static/js/'), filename)


@app.route('/img/<path:filename>')
def img_static(filename):
    return send_from_directory(os.path.join(PROJECT_ROOT, 'static/img/'), filename)


@app.route('/min/<path:filename>')
def min_static(filename):
    return send_from_directory(os.path.join(PROJECT_ROOT, 'static/min/'), filename)


@app.route('/font/<path:filename>')
def font_static(filename):
    return send_from_directory(os.path.join(PROJECT_ROOT, 'static/font/'), filename)


@app.route('/fonts/<path:filename>')
def fonts_static(filename):
    return send_from_directory(os.path.join(PROJECT_ROOT, 'static/fonts/'), filename)


@app.route('/font-awesome/<path:filename>')
def font_awesome_static(filename):
    return send_from_directory(os.path.join(PROJECT_ROOT, 'static/font-awesome/'), filename)


@app.route('/favicon.ico')
def favicon():
    return send_file(os.path.join(PROJECT_ROOT, 'static/favicon.ico'))
