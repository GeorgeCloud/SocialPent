from flask import session, redirect, url_for
from functools import wraps

def current_user():
    return session.get('current_user')

def current_user_is(username):
    """ Checks if current_user's username is true """
    return session['current_user']['username'] == username

def is_authenticated():
    """ Validates if current user is authenticated """
    return True if session.get('username') else False

def login_required(function):
    @wraps(function)
    def wrap(*func, **params):
        print("session:", session)
        if session.get('username'):
            return function(*func, **params)
        return redirect(url_for('explore'))
    return wrap

def logged_out_required(function):
    @wraps(function)
    def wrap(*func, **params):
        if not session.get('current_user'):
            return function(*func, **params)
        return redirect(url_for('explore'))
    return wrap
