from functools import wraps
from flask import session, redirect, url_for
from .models import User


def login_required(func):
    @wraps(func)
    def check_user_login(*args, **kwargs):
        try:
            assert session['login']
        except KeyError:
            session['login'] = False
        finally:
            if session['login'] is True:
                return func(*args, **kwargs)
            else:
                return redirect(url_for('account', msg=2))

    return check_user_login


def logout_required(func):
    @wraps(func)
    def check_user_logout(*args, **kwargs):
        try:
            assert session['login']
        except KeyError:
            session['login'] = False
        finally:
            if session['login'] is False:
                return func(*args, **kwargs)
            else:
                return redirect(url_for('index'))

    return check_user_logout


def login_user(userid):
    session['login'] = True
    session['userid'] = userid


def logout_user():
    session['login'] = False
    session['userid'] = None


def current_user(userid=None):
    if userid is None:
        u = User.query.filter_by(userid=session['userid']).first()
    else:
        u = User.query.filter_by(userid=userid).first()

    return u
