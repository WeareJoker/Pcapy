from flask import session, redirect, url_for
from .models import *


def login_required(func):
    def check_login(*args, **kwargs):
        try:
            session['login']
        except KeyError:
            session['login'] = False
        finally:
            if session['login'] is True:
                return func(*args, **kwargs)
            else:
                return redirect(url_for('account', msg=2))

    return check_login


def logout_required(func):
    def check_logout(*args, **kwargs):
        try:
            session['login']
        except KeyError:
            session['login'] = False
        finally:
            if session['login'] is False:
                return func(*args, **kwargs)
            else:
                return redirect(url_for('account', msg=2))

    return check_logout


def login_user(userid):
    session['login'] = True
    session['userid'] = userid


def logout_user():
    session['login'] = False
    session['userid'] = None


def current_user():
    u = User.query.filter_by(userid=session['userid']).first()
    return u