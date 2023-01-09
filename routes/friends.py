from flask import Blueprint, render_template, request, url_for, redirect, flash, session, jsonify
from helpers.sessions_helper import *
from helpers.user_helper import *
from datetime import datetime
from bson import ObjectId
from db import db

friends_bp = Blueprint('friends_bp', __name__, template_folder='templates')

@friends_bp.route('/create', methods=['POST'])
def create_friend_request():
    current_user = get_current_user()
    session['current_user']['_id'] = ObjectId(current_user['_id'])
    user = db.users.find_one({'username': request.form['username']})

    if not current_user_is(user):
        key = {'sender': current_user['_id'], 'receiver': user['_id']}

        data = {'$set': {'sender'    : current_user['_id'],
                         'receiver'  : user['_id'],
                         'created_on': datetime.now()}}

        db.friend_requests.update_one(key, data, upsert=True)

    return redirect(url_for('users_bp.view_profile', username=user['username']))

@friends_bp.route('/requests', methods=['GET'])
@login_required
def friend_requests():
    current_user = get_db_current_user()

    friends = db.users.find({
        '_id': { '$in': current_user['friends'] }
    }).limit(10)

    requests_sent = db.friend_requests.find({
                        'sender': current_user['_id']})

    sent = [(db.users.find_one({'_id': r['receiver']})['username'],
            (datetime.now() - r['created_on']).days) for r in requests_sent]

    requests_received = db.friend_requests.find({
                        'receiver': current_user['_id']})

    received = [(db.users.find_one({'_id': r['sender']})['username'],
            (datetime.now() - r['created_on']).days) for r in requests_received]

    return render_template('friend_requests.html', friends=friends,
                                                   requests_sent=sent,
                                                   requests_received=received,
                                                   current_user=current_user)

@friends_bp.route('/requests/accept', methods=['POST'])
def accept_friend_request():
    current_user = get_current_user()
    current_user['_id'] = ObjectId(current_user['_id'])

    user = db.users.find_one({'username': request.form['username']})

    friend_request = db.friend_requests.find_one({
                        'sender': user['_id'],
                        'receiver': current_user['_id']})

    if friend_request:
        db.friend_requests.delete_one(friend_request)

        db.users.update_one(current_user, {'$addToSet': {'friends': user['_id']}})

        db.users.update_one(user, {'$addToSet': {'friends': current_user['_id']}})

    return redirect(url_for('friends_bp.friend_requests'))  # Flash message if no user / request

@friends_bp.route('/requests/delete', methods=['POST'])
def delete_friend_request():
    current_user = get_current_user()

    user = db.users.find_one({'username': request.form['username']})

    db.friend_requests.delete_one({
        'sender': ObjectId(current_user['_id']),
        'receiver': user['_id']
    })

    return redirect(request.referrer)
