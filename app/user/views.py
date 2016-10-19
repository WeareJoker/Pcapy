import json

from flask import request, render_template
from sqlalchemy.exc import IntegrityError

from app import app
from app.models import *
from .login_manager import *


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
