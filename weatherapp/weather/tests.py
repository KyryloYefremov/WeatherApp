from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock

from config import API_KEY
from weather.controllers.weather_api import WeatherApi
from weather.views import get_city_forecast


class WeatherViewsTests(TestCase):

    def setUp(self):
        self.default_city = 'Prague'
        self.client = Client()

    @patch.object(WeatherApi, 'get_today_forecast')
    def test_index_view(self, mock_get_today_forecast):
        mock_get_today_forecast.return_value = {
            'mintemp': '15°C',
            'maxtemp': '25°C',
            'condition': 'Sunny',
            'daily_chance_of_rain': '0%',
            'date': '2024-09-01',
        }
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, mock_get_today_forecast.return_value['mintemp'])
        self.assertContains(response, mock_get_today_forecast.return_value['maxtemp'])
        self.assertContains(response, mock_get_today_forecast.return_value['condition'])
        self.assertContains(response, mock_get_today_forecast.return_value['daily_chance_of_rain'])
        self.assertContains(response, mock_get_today_forecast.return_value['date'])
        self.assertContains(response, self.default_city)

    @patch.object(WeatherApi, 'get_today_forecast')
    def test_get_city_forecast_view_success(self, mock_get_today_forecast):
        city = 'Berlin'
        mock_get_today_forecast.return_value = {
            'mintemp': '10°C',
            'maxtemp': '25°C',
            'condition': 'Sunny',
            'daily_chance_of_rain': '10%',
            'date': '2024-09-01',
        }
        response = self.client.get(reverse('get_city_forecast', args=[city]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, mock_get_today_forecast.return_value['mintemp'])
        self.assertContains(response, mock_get_today_forecast.return_value['maxtemp'])
        self.assertContains(response, mock_get_today_forecast.return_value['condition'])
        self.assertContains(response, mock_get_today_forecast.return_value['daily_chance_of_rain'])
        self.assertContains(response, mock_get_today_forecast.return_value['date'])
        self.assertContains(response, city)

    def test_get_city_forecast_view_error(self):
        request = self.client.get(reverse('get_city_forecast', kwargs={'city': 'InvalidCity'}))
        response = get_city_forecast(request, 'InvalidCity')
        self.assertEqual(response.status_code, 200)


class TestWeatherApi(TestCase):

    def setUp(self):
        self.api_key = API_KEY
        self.weather_api = WeatherApi(self.api_key)

    @patch('weather.controllers.weather_api.requests.get')
    def test_get_today_forecast_success(self, mock_get):
        city = 'Prague'
        expected_result = {
            'date': '2024-01-16',
            'condition': 'Sunny',
            'icon_src': 'images/icon-sun.png',
            'maxtemp': 10,
            'mintemp': 5,
            'daily_chance_of_rain': '0%',
            'hourly': [{'00:00': 10}, {'01:00': 9}, {'02:00': 9}]  # Sample hourly forecast
        }

        # Create a mock response object with the expected JSON data and status code
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'forecast': {
                'forecastday': [{
                    'date': '2024-01-16',
                    'day': {
                        'condition': {'text': 'Sunny', 'code': 1000},
                        'maxtemp_c': 10,
                        'mintemp_c': 5,
                        'daily_chance_of_rain': '0%',
                    },
                    'hour': [{'time': '2024-01-16 00:00', 'temp_c': 10},
                             {'time': '2024-01-16 01:00', 'temp_c': 9},
                             {'time': '2024-01-16 02:00', 'temp_c': 9}]
                }]
            }
        }
        mock_get.return_value = mock_response

        # Call the method and check the result
        result = self.weather_api.get_today_forecast(city)
        self.assertEqual(result, expected_result)

    @patch('weather.controllers.weather_api.requests.get')
    def test_get_today_forecast_error(self, mock_get):
        city = 'NonexistentCity'
        # Create a mock response object with a 404 status code
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Check that a ValueError is raised when the city is not found
        with self.assertRaises(ValueError):
            self.weather_api.get_today_forecast(city)
