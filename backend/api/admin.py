from django.contrib import admin
from .models import WeatherData, AirQuality  

# Register your models here.
admin.site.register(WeatherData)
admin.site.register(AirQuality)