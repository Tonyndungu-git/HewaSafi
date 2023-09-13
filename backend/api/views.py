# Import necessary modules
import requests  # For making HTTP requests
import os  # For interacting with the operating system
from django.shortcuts import render, redirect, get_object_or_404  # Django utilities for handling views
from django.contrib.auth import authenticate, login, logout  # Authentication related functions
from django.contrib import messages  # Messages framework for user feedback

# Importing necessary components from your project
from .serializers import WeatherDataSerializer, AirQualitySerializer  # Serializers for converting data to/from JSON
from .models import WeatherData, AirQuality  # Data models for storing weather and air quality information
from .forms import SignUpForm, AirQualityForm, WeatherDataForm  # Forms for user input
from datetime import datetime  # For working with dates and times

# Define the homepage view
def homepage(request):
    # Handle POST request
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)  # Authenticate user
        if user is not None:
            login(request, user)  # Log in user
            messages.success(request, "You Have Been Logged In!")  # Display success message
            return redirect('homepage')  # Redirect to homepage
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again...")  # Display error message
            return redirect('homepage')  # Redirect to homepage
    else:
        return render(request, 'homepage.html')  # Render homepage template

# Define the logout page view
def logout_page(request):
    logout(request)  # Log out user
    messages.success(request, "You Have Been Logged Out...")  # Display logout message
    return redirect('homepage')  # Redirect to homepage

# Define the user registration view
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)  # Create a form instance
        if form.is_valid():
            form.save()  # Save user data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)  # Authenticate user
            login(request, user)  # Log in user
            messages.success(request, "You Have Successfully Registered! Welcome!")  # Display success message
            return redirect('homepage')  # Redirect to homepage
    else:
        form = SignUpForm()  # Create a form instance
        return render(request, 'register.html', {'form':form})  # Render registration template

    return render(request, 'register.html', {'form':form})  # Render registration template

# Define the view for fetching weather data
def weather_data_view(request):
    if request.method == 'POST':
        weather_form = WeatherDataForm(request.POST)  # Create a form instance
        if weather_form.is_valid():
            city = weather_form.cleaned_data['city']
            api_key = '9d37bd3f822a4af6b41100758231908'
            url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}'

            response = requests.get(url)  # Make a request to the API
            if response.status_code == 200:  # Check if request is successful
                data = response.json()  # Convert response to JSON

                # Create a new WeatherData object
                weather_query = WeatherData(
                    user=request.user,
                    timestamp=datetime.now(),
                    city=data['location']['name'],
                    temperature=data['current']['temp_c'],
                    humidity=data['current']['humidity'],
                    wind_speed=data['current']['wind_kph'],
                    condition=data['current']['condition']['text']
                )
                weather_query.save()  # Save the object to the database

                serializer = WeatherDataSerializer(weather_query)  # Serialize data for response

                return render(request, 'weather.html', {'weather_data': serializer.data})  # Render weather template
            else:
                return render(request, 'error_template.html', {'error_message': 'Unable to fetch weather data'})  # Render error template if request fails

    weather_form = WeatherDataForm()  # Create a form instance
    return render(request, 'weather.html', {'weather_form': weather_form})  # Render weather template

# Define the view for fetching air quality data
def air_quality_view(request):
    if request.method == 'POST':
        air_quality_form = AirQualityForm(request.POST)  # Create a form instance
        if air_quality_form.is_valid():
            city = air_quality_form.cleaned_data['city']
            api_key = '9d37bd3f822a4af6b41100758231908'
            air_quality_url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=1&aqi=yes'

            response = requests.get(air_quality_url)  # Make a request to the API
            if response.status_code == 200:  # Check if request is successful
                data = response.json()  # Convert response to JSON
                air_quality = data['current']['air_quality']

                # Create a new AirQuality object
                air_quality_query = AirQuality(
                    user=request.user,
                    timestamp=datetime.now(),
                    city=city,
                    carbon_monoxide=air_quality['co'],
                    ozone=air_quality['o3'],
                    nitrogen_dioxide=air_quality['no2'],
                    sulphur_dioxide=air_quality['so2'],
                    pm2_5=air_quality['pm2_5'],
                    pm10=air_quality['pm10'],
                    us_epa_index=air_quality['us-epa-index'],
                    gb_defra_index=air_quality['gb-defra-index']
                )
                air_quality_query.save()  # Save the object to the database

                serializer = AirQualitySerializer(air_quality_query)  # Serialize data for response

                return render(request, 'airquality.html', {'air_quality_data': serializer.data})  # Render air quality template
            else:
                return render(request, 'error_template.html', {'error_message': 'Unable to fetch air quality data'})  # Render error template if request fails

    air_quality_form = AirQualityForm()  # Create a form instance
    return render(request, 'airquality.html', {'air_quality_form': air_quality_form})  # Render air quality template

# Define weather data list view
def weather_data_list(request):
    if request.method == 'POST':
        selected_records = request.POST.getlist('selected_records')
        WeatherData.objects.filter(pk__in=selected_records).delete()
    #weather_data_list = WeatherData.objects.all()
    user = request.user
    weather_data_list = WeatherData.objects.filter(user=user)

    return render(request, 'weatherdata_list.html', {'weather_data_list': weather_data_list})

# Define air quality view
def air_quality_list(request):
    if request.method == 'POST':
        selected_records = request.POST.getlist('selected_records')
        AirQuality.objects.filter(pk__in=selected_records).delete()
    #air_quality_list = AirQuality.objects.all()
    user = request.user
    air_quality_list = AirQuality.objects.filter(user=user)
    return render(request, 'airquality_list.html', {'air_quality_list': air_quality_list})

# Defines deletion of weather data
def weather_data_delete(request, pk):
    weather_data = get_object_or_404(WeatherData, pk=pk)
    
    if request.method == 'POST':
        weather_data.delete()
        return redirect('weather-data-list')  # Redirect to the list view after successful deletion
    
    return render(request, 'weatherdata_confirm_delete.html', {'weather_data': weather_data})

# Defines deletion of air quality data
def air_quality_delete(request, pk):
    air_quality = get_object_or_404(AirQuality, pk=pk)
    
    if request.method == 'POST':
        air_quality.delete()
        return redirect('air-quality-list')  # Redirect to the list view after successful deletion
    
    return render(request, 'airquality_confirm_delete.html', {'air_quality': air_quality})

# Defines deletion of selected weather data
def delete_selected_weather_data(request):
    if request.method == 'POST':
        selected_records = request.POST.getlist('selected_records')
        WeatherData.objects.filter(pk__in=selected_records, user=request.user).delete()
    return redirect('weather_data_list')

# Defines deletion of selected air quality data
def delete_selected_air_quality(request):
    if request.method == 'POST':
        selected_records = request.POST.getlist('selected_records')
        AirQuality.objects.filter(pk__in=selected_records, user=request.user).delete()
    return redirect('air_quality_list')
