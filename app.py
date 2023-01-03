from flask import render_template, request, url_for, redirect, flash, session, jsonify
from extensions import is_authenticated, current_user
from datetime import datetime
from db import db, app
import requests

from routes.auth import auth_bp
from routes.events import events_bp
from routes.friends import friends_bp
from routes.users import users_bp

app.register_blueprint(auth_bp,    url_prefix='/')
app.register_blueprint(events_bp,  url_prefix='/events')
app.register_blueprint(friends_bp, url_prefix='/friends')
app.register_blueprint(users_bp,   url_prefix='/users')

def is_authenticated():
    return 'username' in session

@app.route('/', methods=['GET'])
def explore():
    if not is_authenticated():
        return redirect(url_for('auth_bp.login'))

    current_user = db.users.find_one({'username': session['username']})
    friends = db.users.find({'_id': {'$in': current_user['friends']}}).limit(5)

    return render_template('explore.html', friends=friends, current_user=current_user)

@app.route('/post', methods=['POST'])
# TODO: add coordinates to post data
def submit_post():
    if not is_authenticated():
        return redirect(url_for('auth_bp.login'))

    current_user = db.users.find_one({'username': session['username']})

    post = dict(user_id=current_user['_id'], message=request.form['message'], created_on=datetime.now())
    db.posts.insert_one(post)

    return redirect(url_for('view_profile', username=current_user['username']))


@app.route('/settings', methods=['GET'])
def user_settings():
    return 'Settings Page in development'

@app.route('/googlemap')
def display_google_map():
    return render_template('googlemap.html')  # Google Map

@app.route('/<username>', methods=['GET'])
def view_profile(username):
    if not is_authenticated():
        return redirect(url_for('auth_bp.login'))

    current_user = db.users.find_one({'username': session['username']})
    user = db.users.find_one({'username': username})

    if user:
        user_posts = db.posts.find({'user_id': user['_id']})
        return render_template('view_profile.html', current_user=current_user, user=user, posts=user_posts)

    else:
        return render_template('404.html', current_user=current_user, error_message=f'{username.capitalize()} Not Found')

if __name__ == '__main__':
    app.run(debug=True)
