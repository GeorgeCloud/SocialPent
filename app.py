from flask import Flask, render_template, request, url_for
from pymongo import MongoClient

app = Flask(__name__)

uri = 'mongodb://localhost:27017/Rando'
client = MongoClient(uri)
db = client.get_default_database()

users = db.users

@app.route('/', methods=['GET'])
def explore():
    return render_template('explore.html')

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
    }

    username = users.insert_one(user).inserted_id

    return render_template(url_for('view_profile'), username=username)

@app.route('/users/<username>', methods=['GET'])
def view_profile(username):
    user = users.find({'username': username})

    return render_template('view_profile.html', user=user)

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)


