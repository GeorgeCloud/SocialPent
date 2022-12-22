from flask import Blueprint

friends_bp = Blueprint('friends_bp', __name__, template_folder='templates')

@friends_bp.route('/add', methods=['POST'])
def create_friend_request():
    # TODO: Handle accepting friend request before sending one.
    current_user = users.find_one({'username': session['username']})
    user = users.find_one({'username': request.form['username']})

    if user:
        key = { 'sender': current_user['_id'], 'receiver': user['_id'] }

        data = {"$set": {
            'sender': current_user['_id'],
            'receiver': user['_id'],
            'created_on': datetime.now()
        }}

        friend_requests.update_one(key, data, upsert=True)

        return redirect(url_for('view_profile', username=user['username']))
    else:
        return 'User Does Not Exist'

@friends_bp.route('/requests', methods=['GET'])
def view_friend_requests():
    if is_authenticated():
        current_user = users.find_one({'username': session['username']})
        requests_sent = friend_requests.find({'sender': current_user['_id']})

        sent = [(users.find_one({'_id': r['receiver']})['username'], (datetime.now() - r['created_on']).days) for r in
                requests_sent]

        requests_received = friend_requests.find({'receiver': current_user['_id']})
        received = [(users.find_one({'_id': r['sender']})['username'], (datetime.now() - r['created_on']).days) for r in
                    requests_received]

        return render_template('friend_requests.html', requests_sent=sent, requests_received=received, current_user=current_user)

    return redirect(url_for('login'))

@friends_bp.route('/requests/accept', methods=['POST'])
def accept_friend_request():
    current_user = users.find_one({'username': session['username']})
    user = users.find_one({'username': request.form['username']})

    friend_request = friend_requests.find_one({'sender': user['_id'], 'receiver': current_user['_id']})

    if friend_request:
        friend_requests.delete_one(friend_request)

        users.update_one(current_user, { '$addToSet': {'friends': user['_id'] } })
        users.update_one(user, {'$addToSet': {'friends': current_user['_id']}})

    # Flash message if no user / request
    return redirect(url_for('view_friend_requests'))

@friends_bp.route('/requests/delete', methods=['POST'])
def delete_friend_request():
    current_user = users.find_one({'username': session['username']})
    user = users.find_one({'username': request.form['username']})

    friend_requests.delete_one({'sender': current_user['_id'], 'receiver': user['_id']})

    return redirect(url_for('view_friend_requests'))
