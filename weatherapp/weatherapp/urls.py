"""
URL configuration for weatherapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from weather import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:city>/<str:forecast_date>/', views.get_city_forecast, name='get_city_forecast'),
    path('search/', views.search_city, name='search_city'),
    path('sign-in/', views.sign_in, name='sign_in'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('sign-out/', views.sign_out, name='sign_out'),
    path('save-city/<str:city>/<str:forecast_date>/', views.save_city, name='save_city'),
    path('remove-city/<str:city>/<str:forecast_date>/', views.remove_city, name='remove_city'),
]
