from django.shortcuts import render
from weather.controllers.weather_api import WeatherApi
from config import API_KEY


def index(request):
    city = 'Prague'
    weather_api = WeatherApi(API_KEY)
    today_forecast = weather_api.get_today_forecast(city)
    today_forecast['city'] = city
    return render(request, 'index.html', context={'today_forecast': today_forecast})
