from flask import Blueprint
from db import db
import bcrypt

users_bp = Blueprint('users_bp', __name__, template_folder='templates')
