from django.urls import path
from .views import weather_data_view, air_quality_view
from . import views

urlpatterns = [
    # Home page
    path('', views.homepage, name='homepage'),

    # Logout page
    path('logout/', views.logout_page, name='logout'),

    # User registration page
    path('register/', views.register_user, name='register'),

    # Weather data view
    path('weather/', views.weather_data_view, name='weather-view'),

    # Air quality view
    path('airquality/', views.air_quality_view, name='air-quality-view'),

    # Weather data list view
    path('weather-data-list/', views.weather_data_list, name='weather-data-list'),

    # Air quality list view
    path('air-quality-list/', views.air_quality_list, name='air-quality-list'),

    # Delete weather data entry
    path('weather-data-delete/<int:pk>/', views.weather_data_delete, name='weather-data-delete'),

    # Delete air quality entry
    path('air-quality-delete/<int:pk>/', views.air_quality_delete, name='air-quality-delete'),
]