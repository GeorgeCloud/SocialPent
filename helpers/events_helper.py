def cleanup_api_data(api_events):
    events = []

    for event in api_events['_embedded']['events']:
        # e_price  = event['priceRanges'][0]
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
                        # 'info'       : event['info'],
                        # 'time'       : e_info['localTime'],
                        # 'address'    : venue_info['address']['line1'],
                        # 'price'      : {'min': e_price['min'], 'max': e_price['max']},
        }
        events.append(event)

        # TODO: Ensure inserting is unique by ID given by TICKETMASTER API
        # Implement background worker

        # db.events.insert_one(event)

    return events
