# weatherapp/views.py
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class GetWeatherByLocation(APIView):
    def get(self, request):
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')

        if not latitude or not longitude:
            return Response({"error": "Please provide both latitude and longitude."}, status=status.HTTP_400_BAD_REQUEST)

        open_meteo_url = 'https://api.open-meteo.com/v1/forecast'
        
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'current_weather': 'true',
        }

        try:
            response = requests.get(open_meteo_url, params=params)

            if response.status_code != 200:
                return Response({"error": "Failed to retrieve data from Open-Meteo."}, status=response.status_code)

            return Response(response.json(), status=status.HTTP_200_OK)

        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
