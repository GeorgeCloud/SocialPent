from datetime import datetime
from db import db

def format_date(date):
    return datetime.fromisoformat(date[:-1]).strftime('%a • %b • %d') # %I:%M %p

def cleanup_api_data(api_events):
    events = []

    for event in api_events['_embedded']['events']:
        e_price    = event.get('priceRanges')
        e_info     = event['dates']['start']
        date       = e_info.get('dateTime')
        venue_info = event['_embedded']['venues'][0]
        event      = {
                        'id'         : event['id'],
                        'name'       : event['name'],
                        'date'       : format_date(date) if date else None,
                        'time'       : e_info,
                        'url'        : event['url'],
                        'image_path' : event['images'][0]['url'],
                        'coordinates': venue_info['location'],
                        'address'    : venue_info.get('address').get('line1'),
                        'type'       : event['type'],
                        'venue_name' : venue_info['name'],
                        'info'       : event.get('info'),
                        'price'      : {'min': e_price[0].get('min'), 'max': e_price[0].get('max')} if e_price else None,
        }
        events.append(event)

        # If new event add to DB.
        db.events.update_one({'id': event['id']}, {'$setOnInsert': event}, upsert=True)

    return events
