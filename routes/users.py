from flask import Blueprint

users_bp = Blueprint('users_bp', __name__, template_folder='templates')

@users_bp.route('/create', methods=['POST'])
def submit_user():
    user = {
        'username': request.form['username'],
        'name': request.form['name'].title(),
        'email': request.form['email'],
        'password': bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt()),
        'friends': [],
    }
    users.insert_one(user)

    return redirect(url_for('view_profile', username=user['username']))

@users_bp.route('/<username>', methods=['GET'])
def view_profile(username):
    if not is_authenticated():
        return redirect(url_for('login'))

    current_user = users.find_one({'username': session['username']})
    user = users.find_one({'username': username})

    if user:
        user_posts = posts.find({'user_id': user['_id']})
        return render_template('view_profile.html', current_user=current_user, user=user, posts=user_posts)

    else:
        return render_template('404.html', current_user=current_user, error_message=f'{username.capitalize()} Not Found')
