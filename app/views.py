#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import render_template, send_file, send_from_directory, request

from . import app
from .config import *
from .long_task import save_pcap


@app.route('/')
def index():
    return render_template('main/index.html')


@app.route('/upload_pcap', methods=['GET', 'POST'])
def upload_pcap():
    if request.method == 'GET':
        return render_template('main/upload_pcap.html')

    elif request.method == 'POST':
        pcap_file = request.files['pcap']

        filename = randomkey(len(pcap_file.filename))
        save_pcap.delay(filename, pcap_file)

        return filename


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
