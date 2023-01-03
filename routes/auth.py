from flask import Blueprint, render_template, request, url_for, redirect, flash, session, jsonify
from extensions import *
from db import db
import bcrypt

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates')

@auth_bp.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET'])
def login():
    if is_authenticated():
        flash('Signed in')
        return redirect(url_for('explore'))

    return render_template('login.html')

@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    session.pop('current_user', None)
    flash('Successfully logged out.')

    return redirect(url_for('auth_bp.login'))

@auth_bp.route('/new-user', methods=['POST'])
def create_user():
    user = {
        'username': request.form['username'],
        'name': request.form['name'].title(),
        'email': request.form['email'],
        'password': bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt()),
        'friends': [],
    }
    db.users.insert_one(user)

    return redirect(url_for('users_bp.view_profile', username=user['username']))

@auth_bp.route('/authenticate', methods=['POST'])
def authenticate():
    if is_authenticated():
        return redirect(url_for('explore'))

    username = request.form['username']
    password = request.form['password']

    user = db.users.find_one({'username': username})

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        del user['password']
        user['_id'] = str(user['_id'])
        session['current_user'] = user

        ### 1:40 am. Need to convert objectid to string and convert string back to objectid when using, or find out if there is an actual issue with session containg objectid or if its a seperate issue.
        ### test having an objectid in session in different locations.

        return redirect(url_for('auth_bp.login'))

    else:
        flash('The password you’ve entered is incorrect.')
        return redirect(url_for('auth_bp.login'))
