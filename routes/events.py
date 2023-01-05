from flask import Blueprint, jsonify
from helpers.events_helper import *
from os import environ
from db import db
import requests

events_bp = Blueprint('events_bp', __name__, template_folder='templates')

# TODO: DB table to keep track of common words in events, update trending -
# TODO: section with terms, delete table data after 1 day.
@events_bp.route('/<coords>', methods=['GET'])
def events(coords):
    TM_API_URL = f'https://app.ticketmaster.com/discovery/v2/events.json?apikey={environ.get("TICKETMASTER_API_KEY")}'
    PARAMS     = {'latlong': coords, 'radius': '1000', 'size': '200'}
    api_events = requests.get(url=TM_API_URL, params=PARAMS).json()
    events     = cleanup_api_data(api_events)

    return jsonify(events)
