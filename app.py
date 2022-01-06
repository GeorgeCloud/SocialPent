from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)

uri = 'mongodb://localhost:27017/Rando'
client = MongoClient(uri)
db = client.get_default_database()

users = db.users
posts = db.posts

current_user = users.find_one({'username': 'fish'})

@app.route('/', methods=['GET'])
def explore():
    # Active Friends
    # Consider only fetching certain data; instead of whole object
    friends = users.find({'_id': {'$in': [ObjectId("61d64a1e141a579f883def9a")]}})
    # Fetch user posts, friends posts, users groups

    # Fetch Google API

    return render_template('explore.html', friends=friends)

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
        'friend_requests_received': [],
        'friend_requests_sent': []
    }
    users.insert_one(user)

    return redirect(url_for('view_profile', username=user['username']))

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']

    user = users.find_one({'username': username})

    if user and user['password'] == password:
        print('signed in')
        return redirect(url_for('view_profile', username=username))
    else:
        # Flash Message: Incorrect Password
        print('password is incorrect')
        return redirect(url_for('login'))

@app.route('/<username>', methods=['GET'])
def view_profile(username):
    user = users.find_one({'username': username})

    user_posts = posts.find({'user_id': user['_id']})

    return render_template('view_profile.html', user=user, posts=user_posts)

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


def add_friend(username):
    # current_user
    # current_user = users.find_one({'username': 'kiirb'})

    user = users.find_one({'username': username})

    if user:
        # Keep track of friend requests sent to users
        users.find_one_and_update(
            {'username': current_user['username']},
            {'$addToSet': {'friend_request_sent': user['_id']}}
        )

        # Friend receives request
        users.find_one_and_update(
            {'username': username},
            {'$addToSet': {'friend_request_received': current_user['_id']}}
        )
    else:
        print('Could not find friend with that username')


if __name__ == '__main__':
    app.run(debug=True)


