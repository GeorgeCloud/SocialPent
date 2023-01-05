from flask import session
from bson import ObjectId
from db import db

def get_current_user():
    """Returns current_user from session."""
    return session.get('current_user')

def _get_db_current_user():
    """Returns current_user from db."""
    current_user_id = session.get('current_user')['_id']

    return db.users.find_one({'_id': ObjectId(current_user_id)})

def current_user_is(user):
    """ Checks if current_user is passed in user."""
    current_user = get_current_user()
    return current_user['username'] == user['username']

def is_friends(user):
    """Returns true if current_user is friends with passed in user instance."""
    db_current_user = _get_db_current_user()

    return user['_id'] in db_current_user['friends']

def request_status(user):
    current_user   = get_current_user()

    sent_req = db.friend_requests.find_one({'sender': ObjectId(current_user['_id']), 'receiver': user['_id']})
    if sent_req: return 'pending'

    incoming_req = db.friend_requests.find_one({'sender': user['_id'], 'receiver': ObjectId(current_user['_id'])})
    if incoming_req: return 'incoming'

    return None
