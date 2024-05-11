from pprint import pprint

import requests
import sys
sys.path.append('../../../')
from config import API_KEY


class WeatherApi:
    """
    Class to interact with the weatherapi.com API.
    """
    def __init__(self, api_key):
        self.__api_key = api_key
        self.__url = 'https://api.weatherapi.com/'

    def get_today_forecast(self, city):
        """
        Get today's forecast for the specified city.
        :param city: City name.
        """

        url = f'{self.__url}v1/forecast.json?key={self.__api_key}&q={city}&days=1&aqi=no&alerts=no'
        response = requests.get(url)
        data = response.json()
        result = {
            'date': data['forecast']['forecastday'][0]['date'],
            'condition': data['forecast']['forecastday'][0]['day']['condition']['text'],
            'maxtemp_c': data['forecast']['forecastday'][0]['day']['maxtemp_c'],
            'mintemp_c': data['forecast']['forecastday'][0]['day']['mintemp_c'],
            'daily_chance_of_rain': data['forecast']['forecastday'][0]['day']['daily_chance_of_rain'],
            'hourly': [{hour['time']: hour['temp_c']} for hour in data['forecast']['forecastday'][0]['hour']]
        }
        return result


wa = WeatherApi(API_KEY)
pprint(wa.get_today_forecast('Liberec'))