import requests

def get_location_from_ip():
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()

        location = data['loc'].split(',')
        latitude = location[0]
        longitude = location[1]

        return latitude, longitude
    except Exception as e:
        return None, None
