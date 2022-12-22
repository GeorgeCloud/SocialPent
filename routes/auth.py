from flask import Blueprint

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates')

@auth_bp.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET'])
def login():
    if is_authenticated():
        # username = session["username"]
        flash('Signed in')
        return redirect(url_for('explore'))

    return render_template('login.html')

@auth_bp.route('/logout', methods=['GET'])
def logout():
    if is_authenticated():
        session.pop('username', None)
        flash('Successfully logged out.')

    return redirect(url_for('login'))

@auth_bp.route('/authenticate', methods=['POST'])
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
