from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import SignUpForm, SignInForm
from .define import DEFAULT_CITY, user, weather_api, user_controller

from datetime import date, timedelta, datetime


def index(request):
    today = date.today().strftime('%Y-%m-%d')
    return get_city_forecast(request, DEFAULT_CITY, today)


def get_city_forecast(request, city, forecast_date):
    try:
        forecast = weather_api.get_forecast(city, forecast_date)
        forecast['city'] = city

        forecast_obj = datetime.strptime(forecast_date, '%Y-%m-%d').date()

        prev_dates, next_dates = [], []
        for i in range(7, 0, -1):
            date_obj = forecast_obj - timedelta(days=i)
            prev_dates.append({
                'date': date_obj.strftime('%Y-%m-%d'),
                'day': date_obj.strftime('%A')
            })
        for i in range(1, 4):
            date_obj = forecast_obj + timedelta(days=i)
            next_dates.append({
                'date': date_obj.strftime('%Y-%m-%d'),
                'day': date_obj.strftime('%A')
            })

        return render(
            request, 'index.html',
            context={'forecast': forecast, 'is_authenticated': user['is_authenticated'],
                     'prev_dates': prev_dates, 'next_dates': next_dates,
                     'nav_cities': user['saved_cities']
                     if user['is_authenticated'] and user['saved_cities'] else [city]})
    except ValueError as e:
        return render(request, 'index-search-error.html', context={'error': e})


def search_city(request):
    city = request.GET.get('city', None)
    if city:
        city = city.title()
        today = date.today().strftime('%Y-%m-%d')
        return redirect('get_city_forecast', city=city, forecast_date=today)


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


def save_city(request, city, forecast_date):
    user['saved_cities'].append(city)
    return redirect('get_city_forecast', city=city, forecast_date=forecast_date)


def remove_city(request, city, forecast_date):
    try:
        user['saved_cities'].remove(city)
    except ValueError:
        pass
    return redirect('get_city_forecast', city=city, forecast_date=forecast_date)


def get_json_forecast(request, city, forecast_date):
    forecast = weather_api.get_forecast(city, forecast_date)
    forecast['city'] = city
    return JsonResponse(forecast)