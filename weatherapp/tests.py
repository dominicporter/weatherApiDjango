from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest import mock

class GetWeatherByLocationTests(APITestCase):
    @mock.patch('weatherapp.views.requests.get')
    def test_get_weather_by_location_success(self, mock_get):
        """
        Ensure the /weather/ endpoint returns weather data when given valid latitude and longitude.
        """
        # Mock response from the Open-Meteo API
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "latitude": 52.52,
            "longitude": 13.405,
            "current_weather": {
                "temperature": 15.2,
                "windspeed": 7.8
            }
        }

        # Make a GET request with valid query parameters
        url = reverse('get_weather_by_location')
        response = self.client.get(url, {'latitude': '52.52', 'longitude': '13.405'})

        # Check that the response is HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check the response data
        self.assertEqual(response.data['latitude'], 52.52)
        self.assertEqual(response.data['longitude'], 13.405)
        self.assertIn('current_weather', response.data)

    def test_get_weather_by_location_missing_params(self):
        """
        Ensure the /weather/ endpoint returns 400 if latitude or longitude is missing.
        """
        url = reverse('get_weather_by_location')
        
        # Make a GET request with missing parameters
        response = self.client.get(url)
        
        # Check that the response is HTTP 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Please provide both latitude and longitude.")
