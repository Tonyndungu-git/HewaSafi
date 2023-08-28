from django.urls import path
from .views import weather_data_view, air_quality_view
#from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    #path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register_user, name='register'),
    path('weather/', views.weather_data_view, name='weather-view'),
    path('airquality/', views.air_quality_view, name='air-quality-view'),
    path('weather-data-list/', views.weather_data_list, name='weather-data-list'),
    path('air-quality-list/', views.air_quality_list, name='air-quality-list'),
    path('weather-data-delete/<int:pk>/', views.weather_data_delete, name='weather-data-delete'),
    path('air-quality-delete/<int:pk>/', views.air_quality_delete, name='air-quality-delete'),


    # path('weather/', weather_data_view_all, name='weather-data-list'),
    # path('airquality/', air_quality_view_all, name='air-quality-list'),
]
