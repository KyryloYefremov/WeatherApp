from django.shortcuts import render, redirect
from weather.controllers.weather_api import WeatherApi

import os

DEFAULT_CITY = 'Prague'
weather_api = WeatherApi(os.getenv('API_KEY'))


def index(request):
    return get_city_forecast(request, DEFAULT_CITY)


def get_city_forecast(request, city):
    try:
        today_forecast = weather_api.get_today_forecast(city)
        today_forecast['city'] = city
        return render(request, 'index.html', context={'today_forecast': today_forecast})
    except ValueError as e:
        return render(request, 'index-search-error.html', context={'error': e})


def search_city(request):
    city = request.GET.get('city', None)
    if city:
        city = city.title()
        return redirect('get_city_forecast', city=city)


def sign_in(request):
    return render(request, 'sign-in.html')


def sign_up(request):
    return render(request, 'sign-up.html')