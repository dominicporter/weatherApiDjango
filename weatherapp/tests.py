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
        mock_response_1 = mock.Mock()
        mock_response_1.status_code = 200
        mock_response_1.json.return_value = [{'lat': '123', 'lon': '456'}]
        
        mock_response_2 = mock.Mock()
        mock_response_2.status_code = 200
        mock_response_2.json.return_value = {
            "latitude": 123,
            "longitude": 456,
            "current_weather": {
                "temperature": 20.5,
                "windspeed": 10.0
            }
        }

        mock_get.side_effect = [mock_response_1, mock_response_2]
        url = reverse('get_weather_by_location')

        # When
        response = self.client.get(url, {'city': 'Edinburgh'})

        # Then
        mock_get.assert_has_calls([
                mock.call('https://nominatim.openstreetmap.org/search?q=Edinburgh&format=json&limit=1',
                          headers={'User-Agent': 'weatherapp'}),
                mock.call('https://api.open-meteo.com/v1/forecast',
                    params={
                        'latitude': '123',
                        'longitude': '456',
                        'current_weather': 'true'
                    }
                )
            ]
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(response.data['latitude'], 123)
        self.assertEqual(response.data['longitude'], 456)
        self.assertIn('current_weather', response.data)
        
    @mock.patch('weatherapp.views.requests.get')
    def test_get_weather_by_city_unknown_city(self, mock_get):
        """
        Ensure the /weather/ endpoint loks up city in external API if not in lookup table.
        """
        # Given
        mock_response_1 = mock.Mock()
        mock_response_1.status_code = 200
        mock_response_1.json.return_value = [{'lat': '123', 'lon': '456'}]
        
        mock_response_2 = mock.Mock()
        mock_response_2.status_code = 200
        mock_response_2.json.return_value = {
            "latitude": 123,
            "longitude": 456,
            "current_weather": {
                "temperature": 20.5,
                "windspeed": 10.0
            }
        }

        mock_get.side_effect = [mock_response_1, mock_response_2]
        url = reverse('get_weather_by_location')

        # When
        response = self.client.get(url, {'city': 'Atlantis'})

        # Then
        mock_get.assert_has_calls([
                mock.call('https://nominatim.openstreetmap.org/search?q=Atlantis&format=json&limit=1',
                          headers={'User-Agent': 'weatherapp'}),
                mock.call('https://api.open-meteo.com/v1/forecast',
                          params={
                    'latitude': '123',
                    'longitude': '456',
                    'current_weather': 'true'
                })
            ]
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(response.data['latitude'], 123)
        self.assertEqual(response.data['longitude'], 456)
        self.assertIn('current_weather', response.data)

    @mock.patch('weatherapp.views.requests.get')
    def test_get_weather_by_city_non_existant_city(self, mock_get):
        """
        Ensure the /weather/ endpoint returns 400 if city isn't known in local lookup, or external API.
        """
        # Given
        mock_get.return_value.json.return_value = None
        url = reverse('get_weather_by_location')

        # When
        response = self.client.get(url, {'city': 'foo'})

        # Then
        mock_get.assert_called_once_with(
            'https://nominatim.openstreetmap.org/search?q=foo&format=json&limit=1',
            headers={'User-Agent': 'weatherapp'}
        )
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
