from flask import Flask, render_template, request, url_for, redirect, flash, session, jsonify
from pymongo import MongoClient
from datetime import datetime
from os import environ
import requests
import bcrypt

app = Flask(__name__)

app.secret_key = b's_s5#y2L"F3%4Q8&sz\n\esc]/'

uri = environ.get('MONGODB_URI', 'mongodb://localhost:27017/reveal')
client = MongoClient(uri)

db = client.get_default_database()

users = db.users
posts = db.posts
friend_requests = db.friendRequests

def is_authenticated():
    return 'username' in session

@app.route('/', methods=['GET'])
def explore():
    if not is_authenticated():
        return redirect(url_for('login'))

    current_user = users.find_one({'username': session['username']})
    friends = users.find({'_id': {'$in': current_user['friends']}}).limit(5)

    return render_template('explore.html', friends=friends, current_user=current_user)

def cleanup_api_data(api_events):
    events = []

    for event in api_events['_embedded']['events']:
        venue_info = event['_embedded']['venues'][0]
        # e_price = event['priceRanges'][0]
        e_info  = event['dates']['start']

        events.append({
            'name'       : event['name'],
            'type'       : event['type'],
            # 'price'      : {'min': e_price['min'], 'max': e_price['max']},
            'date'       : e_info['localDate'],
            # 'time'       : e_info['localTime'],
            'address'    : venue_info['address']['line1'],
            'coordinates': venue_info['location'],
            # 'info'       : event['info'],
            'image_path' : event['images'][0]['url'],
            'url'        : event['url']
        })

    return events

@app.route('/events', methods=['GET'])
def events():
    TM_API_URL = f'https://app.ticketmaster.com/discovery/v2/events.json?apikey={environ.get("TICKETMASTER_API_KEY")}'

    PARAMS = {'city': 'Riverside', 'radius': '500'}

    api_events = requests.get(url=TM_API_URL, params=PARAMS).json()

    events = cleanup_api_data(api_events)

    return jsonify(events)

@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@app.route('/users/create', methods=['POST'])
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

@app.route('/login', methods=['GET'])
def login():
    if is_authenticated():
        # username = session["username"]
        flash('Signed in')
        return redirect(url_for('explore'))

    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    if is_authenticated():
        session.pop('username', None)
        flash('Successfully logged out.')

    return redirect(url_for('login'))

@app.route('/authenticate', methods=['POST'])
def authenticate():
    if is_authenticated():
        return redirect(url_for('login'))  # redirect to explore

    username = request.form['username']
    password = request.form['password']

    user = users.find_one({'username': username})

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        session['username'] = username
        return redirect(url_for('login'))

    else:
        flash('The password you’ve entered is incorrect.')
        return redirect(url_for('login'))


@app.route('/post', methods=['POST'])
def submit_post():
    # Get coordinates of users location
    if not is_authenticated():
        return redirect(url_for('login'))

    current_user = users.find_one({'username': session['username']})

    post = dict(user_id=current_user['_id'], message=request.form['message'], created_on=datetime.now())

    posts.insert_one(post)

    return redirect(url_for('view_profile', username=current_user['username']))

@app.route('/settings', methods=['GET'])
def user_settings():
    return 'Settings Page in development'

@app.route('/<username>', methods=['GET'])
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

@app.route('/friends/add', methods=['POST'])
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

@app.route('/friends/requests', methods=['GET'])
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

@app.route('/friends/requests/accept', methods=['POST'])
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

@app.route('/friends/requests/delete', methods=['POST'])
def delete_friend_request():
    current_user = users.find_one({'username': session['username']})
    user = users.find_one({'username': request.form['username']})

    friend_requests.delete_one({'sender': current_user['_id'], 'receiver': user['_id']})

    return redirect(url_for('view_friend_requests'))

# Google Map
@app.route('/googlemap')
def display_google_map():
    return render_template('googlemap.html')

if __name__ == '__main__':
    app.run(debug=True)
