from flask import Blueprint, render_template, session, request
from helpers.sessions_helper import *
from helpers.user_helper import *
from datetime import datetime
from db import db
from bson import ObjectId
import bcrypt

users_bp = Blueprint('users_bp', __name__, template_folder='templates')

@users_bp.route('', methods=['POST'])
def create_user():
    user = {
        'username': request.form['username'],
        'name': request.form['name'].title(),
        'email': request.form['email'],
        'password': bcrypt.hashpw(request.form['password'].encode('utf-8'),
                                                         bcrypt.gensalt()),
        'friends': [],
    }
    db.users.insert_one(user)

    return redirect(url_for('users_bp.view_profile', username=user['username']))

@users_bp.route('/<username>', methods=['GET'])
@login_required
# TODO: Add bio to user profile, add column to user model
def view_profile(username):
    current_user = get_current_user()
    user = db.users.find_one({'username': username})

    if user:
        user_posts = db.posts.find({'user_id': user['_id']})
        user_posts_cnt = db.posts.count_documents({'user_id': user['_id']})
        return render_template('view_profile.html', current_user=current_user,
                                                    user=user,
                                                    posts=user_posts,
                                                    posts_cnt=user_posts_cnt,
                                                    request_status=request_status(user),
                                                    is_friends=is_friends(user),
                                                    is_owner=current_user_is(user))

    else:
        return render_template('404.html', current_user=current_user,
                                           error_message=f'{username.capitalize()} Not Found')

@users_bp.route('/<username>/post', methods=['POST'])
@login_required
# TODO: add coordinates to post data & image
def create_post(username):
    current_user = get_current_user()

    post = {
            'user_id'    : ObjectId(current_user['_id']),
            'message'    : request.form['message'],
            'created_on' : datetime.now().strftime('%B %d, %Y')
    }

    db.posts.insert_one(post)

    return redirect(url_for('users_bp.view_profile', username=username))

@users_bp.route('/<username>/posts/<post_id>', methods=['GET'])
@login_required
def view_post(username, post_id):
    current_user = get_current_user()
    # Ensure post_id belongs to username
    post = db.posts.find_one({'_id': ObjectId(post_id)})
    return render_template('post_show.html', username=username, post=post, current_user=current_user)

@users_bp.route('/<username>/posts/<post_id>/edit', methods=['GET'])
@login_required
def edit_post(username, post_id):
    current_user = get_current_user()
    user = db.users.find_one({'username': username})
    post = db.posts.find_one({ '$and': [ {'_id': ObjectId(post_id) }, { 'user_id': user['_id'] }] })
    return render_template('post_edit.html', username=username, post=post, current_user=current_user)

@users_bp.route('/<username>/posts/<post_id>/edit', methods=['POST'])
@login_required
def update_post(username, post_id):
    current_user = get_current_user()
    updated_post = {
        'message'    : request.form['message']
    }
    db.posts.update_one(
        {'_id': ObjectId(post_id)},
        {'$set': updated_post}
    )
    return redirect(url_for('users_bp.view_post', username=username, post_id=post_id))

@users_bp.route('/<username>/posts/<post_id>/delete', methods=['POST'])
@login_required
def delete_post(username, post_id):
    current_user = get_current_user()
    db.posts.delete_one({'_id': ObjectId(post_id)})
    return redirect(url_for('users_bp.view_profile', username=username, post_id=post_id, current_user=current_user))
