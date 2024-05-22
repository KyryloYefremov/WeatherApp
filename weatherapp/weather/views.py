from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import SignUpForm, SignInForm

from weather.controllers.weather_api import WeatherApi
from weather.controllers.user_controller import UserController

import os

DEFAULT_CITY = 'Prague'
weather_api = WeatherApi(os.getenv('API_KEY'))
user_controller = UserController('data/users-data.txt')
user = {
    'is_authenticated': False,
    'saved_cities': [],
}


def index(request):
    return get_city_forecast(request, DEFAULT_CITY)


def get_city_forecast(request, city):
    try:
        today_forecast = weather_api.get_today_forecast(city)
        today_forecast['city'] = city
        return render(request, 'index.html', context={'today_forecast': today_forecast, 'user': user})
    except ValueError as e:
        return render(request, 'index-search-error.html', context={'error': e})


def search_city(request):
    city = request.GET.get('city', None)
    if city:
        city = city.title()
        return redirect('get_city_forecast', city=city)


def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            result = user_controller.sign_in(form.cleaned_data['email'], form.cleaned_data['password'])
            if result:
                user['is_authenticated'] = True
                return redirect('index')

    form = SignInForm()
    return render(request, 'sign-in.html', {'form': form})


@csrf_exempt
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            result = user_controller.sign_up(
                form.cleaned_data['email'],
                form.cleaned_data['password'],
                form.cleaned_data['card_number'],
                form.cleaned_data['cvv_code'],
                form.cleaned_data['expiry_date']
            )
            if result:
                user['is_authenticated'] = True
                return redirect('index')

    form = SignUpForm()
    return render(request, 'sign-up.html', {'form': form})


def sign_out(request):
    user['is_authenticated'] = False
    user['saved_cities'] = []
    return redirect('index')