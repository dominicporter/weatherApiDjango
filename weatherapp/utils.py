from django.shortcuts import get_object_or_404
from .models import City
import requests
from rest_framework.response import Response
from rest_framework import status

def get_coordinates(city_name):
    # Check if the city is already in the database
    city = City.objects.filter(name__iexact=city_name).first()
    
    if city:
        # Return stored coordinates if the city is found
        print(f"City found in database: {city_name}")
        return city.latitude, city.longitude
    else:
        print(f"City not in DB, looking it up in API: {city_name}")
        # Fetch coordinates from Nominatim API if the city is not in the database
        nominatim_url = f'https://nominatim.openstreetmap.org/search?q={city_name}&format=json&limit=1'
        response = requests.get(nominatim_url)

        if response.status_code == 200:
            data = response.json()
            if data:
                latitude = data[0]['lat']
                longitude = data[0]['lon']

                # Save the city and its coordinates in the database
                city = City.objects.create(name=city_name, latitude=latitude, longitude=longitude)
                return city.latitude, city.longitude
            else:
                raise ValueError("City not found in Nominatim API.")
        else:
            return None

def get(self, request):
    city_name = request.query_params.get('city')
    if not city_name:
        return Response({"error": "City name is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        latitude, longitude = self.get_coordinates(city_name)
        return Response({"city": city_name, "latitude": latitude, "longitude": longitude})
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
