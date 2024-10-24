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
        # Given
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "latitude": 52.52,
            "longitude": 13.405,
            "current_weather": {
                "temperature": 15.2,
                "windspeed": 7.8
            }
        }
        url = reverse('get_weather_by_location')

        # When
        response = self.client.get(url, {'latitude': '52.52', 'longitude': '13.405'})

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(response.data['latitude'], 52.52)
        self.assertEqual(response.data['longitude'], 13.405)
        self.assertIn('current_weather', response.data)

    @mock.patch('weatherapp.views.requests.get')
    def test_get_weather_by_city_success(self, mock_get):
        """
        Ensure the /weather/ endpoint returns weather data when given valid city.
        """
        # Given
        mock_get.return_value.status_code = 200
        cityLat = 55.9533
        cityLong = -3.1883
        mock_get.return_value.json.return_value = {
            "latitude": cityLat,
            "longitude": cityLong,
            "current_weather": {
                "temperature": 12.34,
                "windspeed": 43.21
            }
        }
        url = reverse('get_weather_by_location')

        # When
        response = self.client.get(url, {'city': 'Edinburgh'})

        # Then
        mock_get.assert_called_once_with(
            'https://api.open-meteo.com/v1/forecast',
            params={
                'latitude': cityLat,
                'longitude': cityLong,
                'current_weather': 'true'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(response.data['latitude'], cityLat)
        self.assertEqual(response.data['longitude'], cityLong)
        self.assertIn('current_weather', response.data)
        
    @mock.patch('weatherapp.views.requests.get')
    def test_get_weather_by_city_unknown_city(self, mock_get):
        """
        Ensure the /weather/ endpoint returns 400 if city is unknown.
        """
        # Given
        # mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = None
        url = reverse('get_weather_by_location')

        # When
        response = self.client.get(url, {'city': 'Atlantis'})

        # Then
        mock_get.assert_not_called()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Unknown city.")


    def test_get_weather_by_location_missing_params(self):
        """
        Ensure the /weather/ endpoint returns 400 if latitude or longitude AND city is missing.
        """
        # Given
        url = reverse('get_weather_by_location')
        
        # When
        response = self.client.get(url)
        
        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Please provide both latitude and longitude, or a city.")
