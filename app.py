from flask import render_template, request, url_for, redirect, flash, session, jsonify
from datetime import datetime
import requests
import bcrypt

from routes.auth import auth_bp
from routes.events import events_bp
from routes.friends import friends_bp
from routes.users import users_bp

from db import db, app

app.register_blueprint(auth_bp,    url_prefix='/')
app.register_blueprint(events_bp,  url_prefix='/events')
app.register_blueprint(friends_bp, url_prefix='/friends')
app.register_blueprint(users_bp,   url_prefix='/users')

def is_authenticated():
    return 'username' in session

@app.route('/', methods=['GET'])
def explore():
    if not is_authenticated():
        return redirect(url_for('login'))

    current_user = db.users.find_one({'username': session['username']})
    friends = db.users.find({'_id': {'$in': current_user['friends']}}).limit(5)

    return render_template('explore.html', friends=friends, current_user=current_user)

@app.route('/post', methods=['POST'])
# TODO: add coordinates to post data
def submit_post():
    if not is_authenticated():
        return redirect(url_for('login'))

    current_user = db.users.find_one({'username': session['username']})

    post = dict(user_id=current_user['_id'], message=request.form['message'], created_on=datetime.now())
    posts.insert_one(post)

    return redirect(url_for('view_profile', username=current_user['username']))

@app.route('/settings', methods=['GET'])
def user_settings():
    return 'Settings Page in development'

@app.route('/googlemap')
def display_google_map():
    return render_template('googlemap.html')  # Google Map

if __name__ == '__main__':
    app.run(debug=True)
