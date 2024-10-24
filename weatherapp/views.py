# weatherapp/views.py
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

def get_coordinates(city_name):
    city_coordinates = {
        'Edinburgh': (55.9533, -3.1883),
        'London': (51.5074, -0.1278),
        'Berlin': (52.52, 13.405),
        'Paris': (48.8566, 2.3522),
        'New York': (40.7128, -74.0060),
        # Add more cities as needed
    }

    # Normalize the city name (case-insensitive) and look it up
    coordinates = city_coordinates.get(city_name.title())
    
    if coordinates:
        return coordinates
    else:
        return None 

class GetWeatherByLocation(APIView):
    def get(self, request):
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')
        city = request.query_params.get('city')

        if not city and (not latitude or not longitude):
            return Response({"error": "Please provide both latitude and longitude, or a city."}, status=status.HTTP_400_BAD_REQUEST)

        open_meteo_url = 'https://api.open-meteo.com/v1/forecast'        


        try:
            # Look up city if necessary
            if city:
                coordinates = get_coordinates(city)
                if not coordinates:
                    return Response({"error": "Unknown city."}, status=status.HTTP_400_BAD_REQUEST)
                latitude, longitude = coordinates

            params = {
                'latitude': latitude,
                'longitude': longitude,
                'current_weather': 'true',
            }

            # Get the weather data from Open-Meteo
            response = requests.get(open_meteo_url, params=params)

            if response.status_code != 200:
                return Response({"error": "Failed to retrieve data from Open-Meteo."}, status=response.status_code)

            return Response(response.json(), status=status.HTTP_200_OK)

        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
