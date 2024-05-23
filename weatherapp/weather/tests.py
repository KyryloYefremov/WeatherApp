import os
import tempfile
from datetime import date, timedelta

from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock

from weather.controllers.user_controller import UserController
from weather.controllers.weather_api import WeatherApi
from weather.views import get_city_forecast


class WeatherViewsTests(TestCase):

    def setUp(self):
        self.default_city = 'Prague'
        self.client = Client()

    @patch.object(WeatherApi, 'get_forecast')
    def test_index_view(self, mock_get_forecast):
        mock_get_forecast.return_value = {
            'mintemp': '15°C',
            'maxtemp': '25°C',
            'condition': 'Sunny',
            'daily_chance_of_rain': '0%',
            'date': '2024-09-01',
        }
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, mock_get_forecast.return_value['mintemp'])
        self.assertContains(response, mock_get_forecast.return_value['maxtemp'])
        self.assertContains(response, mock_get_forecast.return_value['condition'])
        self.assertContains(response, mock_get_forecast.return_value['daily_chance_of_rain'])
        self.assertContains(response, mock_get_forecast.return_value['date'])
        self.assertContains(response, self.default_city)

    @patch.object(WeatherApi, 'get_forecast')
    def test_get_city_forecast_view_success(self, mock_get_forecast):
        city = 'Berlin'
        mock_get_forecast.return_value = {
            'mintemp': '10°C',
            'maxtemp': '25°C',
            'condition': 'Sunny',
            'daily_chance_of_rain': '10%',
            'date': '2024-09-01',
        }
        response = self.client.get(reverse('get_city_forecast', args=[city, date.today().strftime('%Y-%m-%d')]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, mock_get_forecast.return_value['mintemp'])
        self.assertContains(response, mock_get_forecast.return_value['maxtemp'])
        self.assertContains(response, mock_get_forecast.return_value['condition'])
        self.assertContains(response, mock_get_forecast.return_value['daily_chance_of_rain'])
        self.assertContains(response, mock_get_forecast.return_value['date'])
        self.assertContains(response, city)

    def test_get_city_forecast_view_error(self):
        request = self.client.get(reverse('get_city_forecast',
                                          kwargs={'city': 'InvalidCity',
                                                  'forecast_date': date.today().strftime('%Y-%m-%d')}))
        response = get_city_forecast(request, 'InvalidCity', date.today().strftime('%Y-%m-%d'))
        self.assertEqual(response.status_code, 200)


class TestWeatherApi(TestCase):

    def setUp(self):
        self.api_key = 'test_key'
        self.weather_api = WeatherApi(self.api_key)

    @patch('weather.controllers.weather_api.requests.get')
    def test_get_forecast_history_success(self, mock_get):
        city = 'Prague'
        forecast_date = (date.today() - timedelta(days=3)).strftime('%Y-%m-%d')
        expected_result = {
            'date': forecast_date,
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
                    'date': forecast_date,
                    'day': {
                        'condition': {'text': 'Sunny', 'code': 1000},
                        'maxtemp_c': 10,
                        'mintemp_c': 5,
                        'daily_chance_of_rain': '0%',
                    },
                    'hour': [{'time': '2023-01-16 00:00', 'temp_c': 10},
                             {'time': '2023-01-16 01:00', 'temp_c': 9},
                             {'time': '2023-01-16 02:00', 'temp_c': 9}]
                }]
            }
        }
        mock_get.return_value = mock_response

        # Call the method and check the result
        result = self.weather_api.get_forecast(city, forecast_date)
        self.assertEqual(result, expected_result)

    @patch('weather.controllers.weather_api.requests.get')
    def test_get_forecast_future_success(self, mock_get):
        city = 'Prague'
        forecast_date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        expected_result = {
            'date': forecast_date,
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
                    'date': forecast_date,
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
        result = self.weather_api.get_forecast(city, forecast_date)
        self.assertEqual(result, expected_result)

    @patch('weather.controllers.weather_api.requests.get')
    def test_get_forecast_error(self, mock_get):
        city = 'NonexistentCity'
        forecast_date = '2024-01-16'
        # Create a mock response object with a 404 status code
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Check that a ValueError is raised when the city is not found
        with self.assertRaises(ValueError):
            self.weather_api.get_forecast(city, forecast_date)

    @patch('weather.controllers.weather_api.requests.get')
    def test_get_history(self, mock_get):
        city = 'Prague'
        forecast_date = (date.today() - timedelta(days=2)).strftime('%Y-%m-%d')

        # Create a mock response object
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Call the method
        response = self.weather_api._WeatherApi__get_history(city, forecast_date)

        # Check that the requests.get method was called with the correct URL
        mock_get.assert_called_once_with(f'https://api.weatherapi.com/v1/history.json?'
                                         f'key=test_key&q=Prague&dt={forecast_date}')
        self.assertEqual(response, mock_response)

    @patch('weather.controllers.weather_api.requests.get')
    def test_get_future(self, mock_get):
        city = 'Prague'
        forecast_date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')

        # Create a mock response object
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Call the method
        response = self.weather_api._WeatherApi__get_future(city, forecast_date)

        # Check that the requests.get method was called with the correct URL
        mock_get.assert_called_once_with(f'https://api.weatherapi.com/v1/forecast.json?'
                                         f'key=test_key&q=Prague&dt={forecast_date}')
        self.assertEqual(response, mock_response)


class TestUserController(TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.user_controller = UserController(self.temp_file.name)

    def tearDown(self):
        os.remove(self.temp_file.name)

    def test_sign_up_and_sign_in(self):
        email = "test@example.com"
        password = "password123"
        card_number = "1234567812345678"
        cvv = "123"
        expiration_date = "12/24"

        # Test sign up with correct data
        self.assertTrue(self.user_controller.sign_up(email, password, card_number, cvv, expiration_date))

        # Test sign in with correct password
        self.assertTrue(self.user_controller.sign_in(email, password))

        # Test sign in with wrong password
        self.assertFalse(self.user_controller.sign_in(email, "wrongpassword"))

    def test_sign_up_invalid_data(self):
        email = "test@example.com"
        password = "password123"
        card_number = "1234"  # Wrong card number
        cvv = "12"            # Wrong CVV
        expiration_date = "1224"  # Wrong expiration date

        self.assertFalse(self.user_controller.sign_up(email, password, card_number, cvv, expiration_date))

    def test_sign_in_non_existent_user(self):
        # Test sign in with non-existent email
        self.assertFalse(self.user_controller.sign_in("nonexistent@example.com", "password"))