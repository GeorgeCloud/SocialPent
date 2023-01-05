def cleanup_api_data(api_events):
    events = []

    for event in api_events['_embedded']['events']:
        e_price    = event.get('priceRanges')
        e_info     = event['dates']['start']
        venue_info = event['_embedded']['venues'][0]
        event      = {
                        'name'       : event['name'],
                        'type'       : event['type'],
                        'date'       : e_info['localDate'],
                        'coordinates': venue_info['location'],
                        'image_path' : event['images'][0]['url'],
                        'url'        : event['url'],

                        # API returns events with missing data
                        'info'       : event.get('info'),
                        'time'       : e_info,
                        'address'    : venue_info.get('address').get('line1'),
                        'price'      : {'min': e_price[0].get('min'), 'max': e_price[0].get('max')} if e_price else None,
        }
        events.append(event)

        # TODO: Ensure inserting is unique by ID given by TICKETMASTER API
        # Implement background worker

        # db.events.insert_one(event)

    return events
