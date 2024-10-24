import requests

def get_coordinates(city_name):
    city_coordinates = {
        'Edinburgh': (55.9533, -3.1883),
        'London': (51.5074, -0.1278),
        'Berlin': (52.52, 13.405),
        'Paris': (48.8566, 2.3522),
        'New York': (40.7128, -74.0060),
    }

    # Normalize the city name (case-insensitive) and look it up
    coordinates = city_coordinates.get(city_name.title())
    
    if coordinates:
        return coordinates
    else:
        return get_coordinates_from_api(city_name)

def get_coordinates_from_api(city_name):
    url = 'https://nominatim.openstreetmap.org/search'
    
    params = {
        'q': city_name,
        'format': 'json',
        'limit': 1
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()

            if data:
                latitude = data[0]['lat']
                longitude = data[0]['lon']
                return float(latitude), float(longitude)
            else:
                return None
        else:
            return None

    except requests.RequestException as e:
        print(f"Error: {e}")
        return None
