from flask import session, redirect, url_for
from functools import wraps
from bson import ObjectId
from db import db


def get_current_user():
    return session.get('current_user')

def is_authenticated():
    """ Returns true if logged in else False """
    return get_current_user()

def current_user_is(username):
    """ Checks if current_user's username is value passed in """
    current_user = get_current_user()
    return currnent_user['username'] == username

def is_friends(user):
    """ Returns true if current_user is friends with passed in user instance"""
    current_user = get_current_user()
    db_current_user = db.users.find_one({'_id': ObjectId(current_user['_id'])})

    return user['_id'] in db_current_user['friends']

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
