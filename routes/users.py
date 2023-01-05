from flask import Blueprint, render_template, session, request
from helpers.sessions_helper import *
from helpers.user_helper import *
from datetime import datetime
from db import db
import bcrypt

users_bp = Blueprint('users_bp', __name__, template_folder='templates')

@users_bp.route('/<username>', methods=['GET'])
@login_required
# TODO: Add bio to user profile, add column to user model
def view_profile(username):
    current_user = get_current_user()
    user = db.users.find_one({'username': username})

    if user:
        user_posts = db.posts.find({'user_id': user['_id']})
        return render_template('view_profile.html', current_user=current_user,
                                                    user=user,
                                                    posts=user_posts,
                                                    request_status=request_status(user),
                                                    is_friends=is_friends(user),
                                                    is_owner=current_user_is(user))

    else:
        return render_template('404.html', current_user=current_user,
                                           error_message=f'{username.capitalize()} Not Found')

@users_bp.route('/<username>/post', methods=['POST'])
@login_required
# TODO: add coordinates to post data
# TODO: create edit/delete route for posts
def create_post(username):
    current_user = get_current_user()

    current_user = db.users.find_one({'username': username})

    post = {
            'user_id'    : current_user['_id'],
            'message'    : request.form['message'],
            'created_on' : datetime.now()
    }

    db.posts.insert_one(post)

    return redirect(url_for('users_bp.view_profile', username=username))
