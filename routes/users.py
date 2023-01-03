from flask import Blueprint, render_template, session
from extensions import *
from db import db
import bcrypt

users_bp = Blueprint('users_bp', __name__, template_folder='templates')

@users_bp.route('/<username>', methods=['GET'])
@login_required
def view_profile(username):
    if not is_authenticated():
        return redirect(url_for('auth_bp.login'))

    current_user = get_current_user()
    user = db.users.find_one({'username': username})

    if user:
        user_posts = db.posts.find({'user_id': user['_id']})
        return render_template('view_profile.html', current_user=current_user,
                                                    user=user,
                                                    posts=user_posts,
                                                    is_friends=is_friends(user))

    else:
        return render_template('404.html', current_user=current_user,
                                           error_message=f'{username.capitalize()} Not Found')

@users_bp.route('/post', methods=['POST'])
# TODO: add coordinates to post data
def submit_post():
    if not is_authenticated():
        return redirect(url_for('auth_bp.login'))

    current_user = db.users.find_one({'username': session['username']})

    post = dict(user_id=current_user['_id'], message=request.form['message'],
            created_on=datetime.now())

    db.posts.insert_one(post)

    return redirect(url_for('users_bp.view_profile', username=current_user['username']))
