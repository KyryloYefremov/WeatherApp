from config import API_KEY
from weather.controllers.user_controller import UserController
from weather.controllers.weather_api import WeatherApi

DEFAULT_CITY = 'Prague'
weather_api = WeatherApi(API_KEY)
user_controller = UserController('weather/data/users-data.txt')
user = {
    'is_authenticated': False,
    'saved_cities': ['Berlin', 'Liberec']
}