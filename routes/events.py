from flask import Blueprint, jsonify
from extensions import *
from os import environ
from db import db
import requests

events_bp = Blueprint('events_bp', __name__, template_folder='templates')

# TODO: DB table to keep track of common words in events, update trending -
# TODO: section with terms, delete table data after 1 day.
def cleanup_api_data(api_events):
    events = []

    for event in api_events['_embedded']['events']:
        e_info  = event['dates']['start']
        # e_price = event['priceRanges'][0]
        venue_info = event['_embedded']['venues'][0]

        events.append({
            'name'       : event['name'],
            'type'       : event['type'],
            'date'       : e_info['localDate'],
            'coordinates': venue_info['location'],
            'image_path' : event['images'][0]['url'],
            'url'        : event['url']

            # 'info'       : event['info'],
            # 'time'       : e_info['localTime'],
            # 'address'    : venue_info['address']['line1'],  # Some event data has no address
            # 'price'      : {'min': e_price['min'], 'max': e_price['max']},
        })

    return events

@events_bp.route('/<coords>', methods=['GET'])
def events(coords):
    TM_API_URL = f'https://app.ticketmaster.com/discovery/v2/events.json?apikey={environ.get("TICKETMASTER_API_KEY")}'
    PARAMS     = {'latlong': coords, 'radius': '1000', 'size': '200'}
    api_events = requests.get(url=TM_API_URL, params=PARAMS).json()

    events     = cleanup_api_data(api_events)
    return jsonify(events)
