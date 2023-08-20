from django.urls import path
from .views import weather_data_view, weather_data_view_all, air_quality_view_all, air_quality_view

urlpatterns = [
    path('weather/<str:city>/', weather_data_view, name='weather-view'),
    path('air_quality/<str:city>/', air_quality_view, name='air-quality-view'),
    path('weather/', weather_data_view_all, name='weather-data-list'),
    path('air_quality/', air_quality_view_all, name='air-quality-list'),
]
