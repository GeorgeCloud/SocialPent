from flask import render_template, request, url_for, redirect, flash, session, jsonify
from extensions import *
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
app.register_blueprint(users_bp,   url_prefix='/u')

@app.route('/', methods=['GET'])
@login_required
def explore():
    current_user = get_current_user()

    db_current_user = db.users.find_one({'username': current_user['username']})  # db_current_user has all db properties: friends, etc.
    friends = db.users.find({'_id': {'$in': db_current_user['friends']}}).limit(5)

    return render_template('explore.html', friends=friends, current_user=db_current_user)

@app.route('/settings', methods=['GET'])
def user_settings():
    return 'Settings Page in development'

@app.route('/googlemap')
def display_google_map():
    return render_template('googlemap.html')  # Google Map

if __name__ == '__main__':
    app.run(debug=True)
