from flask import Blueprint

friend_requests_bp = Blueprint('friend_requests', __name__, template_folder='templates')

# Move friend requests routes to blueprint
