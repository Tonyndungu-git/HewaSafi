from rest_framework import serializers
from .models import WeatherData, AirQuality

class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = '__all__'
        verbose_name_plural = 'Weather Data'

class AirQualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = AirQuality
        fields = '__all__'
        verbose_name_plural = 'Air Quality'  