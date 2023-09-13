from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



# WEATHER DATA MODEL
class WeatherData(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    city = models.CharField(max_length=100, default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    humidity = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    wind_speed = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    condition = models.CharField(max_length=100)

    def __str__(self):
        return f"Weather data for {self.city} at {self.timestamp}"

# AIR QUALITY MODEL
class AirQuality(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    city = models.CharField(max_length=100, default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    carbon_monoxide = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    ozone = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    nitrogen_dioxide = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    sulphur_dioxide = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    pm2_5 = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    pm10 = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    us_epa_index = models.IntegerField()
    gb_defra_index = models.IntegerField()

    def __str__(self):
        return f"Air Quality for {self.city} at {self.timestamp}"
