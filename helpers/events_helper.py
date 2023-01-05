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
