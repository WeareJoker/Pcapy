#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import json

from flask import render_template, send_file, send_from_directory
from flask import stream_with_context, request, Response
from sqlalchemy.exc import IntegrityError
from .long_task import analysis_pcap

from . import app, db
from .config import *
from .login_manager import *
from .models import *

try:
    import MySQLdb
except ImportError:
    import pymysql

    pymysql.install_as_MySQLdb()


@app.route('/stream')
def streamed_response():
    def generate():
        yield 'Hello '
        time.sleep(2)
        yield request.args['name']
        time.sleep(3)
        yield '!'

    return Response(stream_with_context(generate()))


@app.route('/')
def index():
    return redirect(url_for('upload_pcap'))


@app.route('/result/<string:pcapname>')
@login_required
def result(pcapname):
    u = current_user()
    p = Pcap.query.filter_by(fake_filename=pcapname, user=u).first()
    if p is None:
        return "<script>alert('잘못된 접근입니다!');history.go(-1);</script>"
    else:
        return render_template('main/index.html',
                               pcap=p,
                               user_pcap=u.pcap)


@app.route('/pcap/upload', methods=['GET', 'POST'])
@login_required
def upload_pcap():
    if request.method == 'GET':
        u = current_user()
        return render_template('main/upload_pcap.html',
                               pcap_id=randomkey(30),
                               user_pcap=u.pcap)

    elif request.method == 'POST':
        pcap_file = request.files['pcap']

        filetype = pcap_file.filename.split('.')[-1]
        fake_filename = randomkey(len(pcap_file.filename)) + '.' + filetype
        filepath = os.path.join(PCAP_FILE_PATH, fake_filename)
        pcap_file.save(filepath)
        u = current_user()

        p = Pcap(fake_filename, pcap_file.filename, u)

        add_and_commit(db.session, p)

        u.pcap.append(p)

        db.session.commit()

        analysis_pcap.delay(filepath, u.userid)

        return fake_filename


@app.route('/user/account', methods=['GET', 'POST'])
@logout_required
def account():
    if request.method == 'GET':
        msg_list = list()

        msg = request.args.get('msg')
        if msg is not None:
            msg_list.append({
                                '1': '잘못된 아이디 혹은 패스워드 입니다.',
                                '2': '로그인이 필요합니다.',
                                '3': '회원가입을 성공하였습니다.'
                            }.get(msg))
        return render_template('main/login.html',
                               alert_message_list=msg_list)

    if request.method == 'POST':
        data = request.form

        u = User(data['userid'], data['userpw'])
        try:
            add_and_commit(db.session, u)
        except IntegrityError:
            return redirect(url_for('account', msg=1))

        return redirect(url_for('account', msg=3))


@app.route('/user/alarm', methods=['GET'])
@login_required
def alarm():
    u = current_user()
    data = dict()

    alarms = Alarm.query.filter_by(user=u).order_by(Alarm.time).limit(5).all()

    for a, idx in zip(alarms, reversed(range(len(alarms)))):
        data[idx] = [a.type, a.simple_content]

    return json.dumps(data)


@app.route('/user/login', methods=['POST'])
@logout_required
def login():
    data = request.form
    if request.method == 'POST':
        u = User.query.filter_by(userid=data['userid'], userpw=data['userpw']).first()
        if u is None:
            return redirect(url_for('account', msg=1))
        else:
            login_user(u.userid)
            return redirect(url_for('index'))

    elif request.method == 'DELETE':
        logout_user()


@app.route('/user/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('account'))


from .static_view import *
