from django.urls import path
from .views import GetWeatherByLocation

urlpatterns = [
    path('weather/', GetWeatherByLocation.as_view(), name='get_weather_by_location'),
]
