from flask import Blueprint, jsonify
from os import environ
import requests

events_bp = Blueprint('events_bp', __name__, template_folder='templates')

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
            # 'address'    : venue_info['address']['line1'],  # Some event data has no address
            'coordinates': venue_info['location'],
            # 'info'       : event['info'],
            'image_path' : event['images'][0]['url'],
            'url'        : event['url']
        })

    return events

@events_bp.route('/<coords>', methods=['GET'])
def events(coords):
    TM_API_URL = f'https://app.ticketmaster.com/discovery/v2/events.json?apikey={environ.get("TICKETMASTER_API_KEY")}'

    PARAMS = {'latlong': coords, 'radius': '1000', 'size': '200'}

    api_events = requests.get(url=TM_API_URL, params=PARAMS).json()

    events = cleanup_api_data(api_events)

    return jsonify(events)
