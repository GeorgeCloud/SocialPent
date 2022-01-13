from flask import Flask, render_template, request, url_for, redirect, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime


app = Flask(__name__)
app.secret_key = b's_s5#y2L"F3%4Q8&sz\n\esc]/'

uri = 'mongodb://localhost:27017/Rando'
client = MongoClient(uri)
db = client.get_default_database()

users = db.users
posts = db.posts
friend_requests = db.friendRequests

current_user = users.find_one({'username': 'kiirb'})

@app.route('/', methods=['GET'])
def explore():
    # Active Friends
    # Consider only fetching certain data(username, status); instead of entire object
    friends = users.find({'_id': {'$in': current_user['friends']}}).limit(5)
    # Aggregate current_user posts, friends posts,

    # Fetch Google API

    return render_template('explore.html', friends=friends, current_user=current_user)

@app.route('/signup', methods=['GET'])
def new_user():
    return render_template('new_user.html')

@app.route('/users/create', methods=['POST'])
def submit_user():
    user = {
        'username': request.form['username'],
        'name': request.form['name'].title(),
        'email': request.form['email'],
        'password': request.form['password'],
        'friends': [],
    }
    users.insert_one(user)

    return redirect(url_for('view_profile', username=user['username']))

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    return redirect(url_for('login'))

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']

    user = users.find_one({'username': username})

    if user and user['password'] == password:
        flash('Signed in')
        return redirect(url_for('explore'))
    else:
        # Flash Message: Incorrect Password
        print('password is incorrect')
        return redirect(url_for('login'))

# @app.route('/friends', methods=['GET'])
# def get_friends():
#     return loads(users.find(
#         {'_id': {'$in': [current_user['_id']]}}
#     ))

@app.route('/post', methods=['POST'])
def submit_post():
    # Get coordinates of users location

    # current_user
    user = users.find_one({'username': 'kiirb'})

    post = {
        'user_id': user['_id'],
        'message': request.form['message'],
        'created_on': datetime.now(),
    }

    posts.insert_one(post)

    return redirect(url_for('view_profile', username=user['username']))

@app.route('/settings', methods=['GET'])
def user_settings():
    return 'Settings Page in development'

@app.route('/<username>', methods=['GET'])
def view_profile(username):
    user = users.find_one({'username': username})

    if user:
        user_posts = posts.find({'user_id': user['_id']})
        return render_template('view_profile.html', user=user, posts=user_posts)

    else:
        return render_template('404.html', error_message=f'{username.capitalize()} Not Found')

@app.route('/friends/add', methods=['POST'])
def create_friend_request():
    # TODO: Handle accepting friend request before sending one.
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

@app.route('/friends/requests', methods=['GET'])
def view_friend_requests():
    requests_sent = friend_requests.find({'sender': current_user['_id']})
    sent = [(users.find_one({'_id': r['receiver']})['username'], (datetime.now() - r['created_on']).days) for r in
            requests_sent]

    requests_received = friend_requests.find({'receiver': current_user['_id']})
    received = [(users.find_one({'_id': r['sender']})['username'], (datetime.now() - r['created_on']).days) for r in
                requests_received]

    return render_template('friend_requests.html', requests_sent=sent, requests_received=received)

@app.route('/friends/requests/accept', methods=['POST'])
def accept_friend_request():
    user = users.find_one({'username': request.form['username']})

    friend_request = friend_requests.find_one({'sender': user['_id'], 'receiver': current_user['_id']})

    if friend_request:
        friend_requests.delete_one(friend_request)

        users.update_one(current_user, { '$addToSet': {'friends': user['_id'] } })
        users.update_one(user, {'$addToSet': {'friends': current_user['_id']}})

    # Flash message if no user / request
    return redirect(url_for('view_friend_requests'))

@app.route('/friends/requests/delete', methods=['POST'])
def delete_friend_request():
    user = users.find_one({'username': request.form['username']})

    friend_requests.delete_one({'sender': current_user['_id'], 'receiver': user['_id']})

    return redirect(url_for('view_friend_requests'))


if __name__ == '__main__':
    app.run(debug=True)
