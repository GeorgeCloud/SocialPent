from flask import session, redirect, url_for
from functools import wraps

def login_required(function):
    @wraps(function)
    def wrap(*func, **params):
        if session.get('current_user'):
            return function(*func, **params)
        return redirect(url_for('auth_bp.login'))
    return wrap

def logged_out_required(function):
    @wraps(function)
    def wrap(*func, **params):
        if not session.get('current_user'):
            return function(*func, **params)
        return redirect(url_for('explore'))
    return wrap
