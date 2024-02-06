from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from weather.views import weather_info_api, get_lat_lon_from_nominatim, cache 
from demo.settings import base

REST_FRAMEWORK = {}

class WeatherApiTest(TestCase):

    @patch('get_lat_lon_from_nominatim')
    @patch('requests.get')
    @patch('cache.get')
    @patch('cache.set')
    def test_weather_info_api_success(self, mock_cache_set, mock_cache_get, mock_requests_get, mock_get_lat_lon_from_nominatim):
        mock_cache_get.return_value = None
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = {
            'main': {'temp': 25.5},
            'wind': {'speed': 5, 'deg': 180},
            'weather': [{'description': 'Clear sky'}]
        }
        mock_get_lat_lon_from_nominatim.return_value = (0.0, 0.0)

        url = reverse('weather_info_api')
        response = self.client.get(url, {'city': 'Paris'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather.html')
        self.assertContains(response, 'Paris')
        self.assertContains(response, '25.5')

        mock_cache_set.assert_called_once()

    @patch('weather.views.get_lat_lon_from_nominatim')
    @patch('weather.views.requests.get')
    @patch('weather.views.cache.get')
    def test_weather_info_api_cache_hit(self, mock_cache_get, mock_requests_get, mock_get_lat_lon_from_nominatim):
        mock_cache_get.return_value = {
            'city': 'Paris',
            'current_temperature': 25.5,
            'min_temperature': 20.0,
            'max_temperature': 30.0,
            'humidity': 60,
            'pressure': 1010,
            'wind_speed': 5,
            'wind_direction': 'S',
            'description': 'Clear sky'
        }

        url = reverse('weather_info_api')
        response = self.client.get(url, {'city': 'Paris'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather.html')
        self.assertContains(response, 'Paris')
        self.assertContains(response, '25.5')
        self.assertNotContains(response, 'Error fetching weather information')

    @patch('weather.views.get_lat_lon_from_nominatim')
    @patch('weather.views.requests.get')
    def test_weather_info_api_error(self, mock_requests_get, mock_get_lat_lon_from_nominatim):
        mock_requests_get.return_value.status_code = 404
        mock_get_lat_lon_from_nominatim.return_value = (0.0, 0.0)

        url = reverse('weather_info_api')
        response = self.client.get(url, {'city': 'InvalidCity'})

        self.assertEqual(response.status_code, 500)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {'error': 'Error fetching weather information'})

    def test_weather_info_api_missing_city(self):
        url = reverse('weather_info_api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {'error': 'City is required'})
