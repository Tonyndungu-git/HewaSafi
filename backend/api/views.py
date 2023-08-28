import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# from rest_framework import permissions, authentication
# from rest_framework import generics
# from rest_framework.response import Response
from .serializers import WeatherDataSerializer, AirQualitySerializer
from .models import WeatherData, AirQuality
from .forms import SignUpForm, AirQualityForm, WeatherDataForm
from datetime import datetime


#from .permission import IsStaffEditorPermission


def homepage(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		# Authenticate
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You Have Been Logged In!")
			return redirect('homepage')
		else:
			messages.success(request, "There Was An Error Logging In, Please Try Again...")
			return redirect('homepage')
	else:
		return render(request, 'homepage.html')

    
    #return render(request, 'homepage.html', {})



def logout_page(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out...")
	return redirect('homepage')

def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('homepage')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})


# def weather_data_view(request):
#     if request.method == 'POST':
#         weather_form = WeatherDataForm(request.POST)
#         if weather_form.is_valid():
#             city = weather_form.cleaned_data['city']
#             return redirect('weather-data-api', city=city)  # Redirect to the API view
#     else:
#         weather_form = WeatherDataForm()
    
#     return render(request, 'weather.html', {'form': weather_form})

# def air_quality_view(request):
#     if request.method == 'POST':
#         air_quality_form = AirQualityForm(request.POST)
#         if air_quality_form.is_valid():
#             city = air_quality_form.cleaned_data['city']
#             return redirect('air-quality-api', city=city)  # Redirect to the API view
#     else:
#         air_quality_form = AirQualityForm()
    
#     return render(request, 'air_quality.html', {'air_quality_form': air_quality_form})


def weather_data_view(request):
    if request.method == 'POST':
        weather_form = WeatherDataForm(request.POST)
        if weather_form.is_valid():
            city = weather_form.cleaned_data['city']
            api_key = '9d37bd3f822a4af6b41100758231908'
            url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}'

            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()

                weather_query = WeatherData(
                    user=request.user,
                    timestamp=datetime.now(),
                    city=data['location']['name'],
                    temperature=data['current']['temp_c'],
                    humidity=data['current']['humidity'],
                    wind_speed=data['current']['wind_kph'],
                    condition=data['current']['condition']['text']
                )
                weather_query.save()

                serializer = WeatherDataSerializer(weather_query)

                return render(request, 'weather.html', {'weather_data': serializer.data})
            else:
                return render(request, 'error_template.html', {'error_message': 'Unable to fetch weather data'})

    weather_form = WeatherDataForm()
    return render(request, 'weather.html', {'weather_form': weather_form})

def air_quality_view(request):
    if request.method == 'POST':
        air_quality_form = AirQualityForm(request.POST)
        if air_quality_form.is_valid():
            city = air_quality_form.cleaned_data['city']
            api_key = '9d37bd3f822a4af6b41100758231908'
            air_quality_url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=1&aqi=yes'

            response = requests.get(air_quality_url)
            if response.status_code == 200:
                data = response.json()
                air_quality = data['current']['air_quality']

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
                air_quality_query.save()

                serializer = AirQualitySerializer(air_quality_query)
                return render(request, 'airquality.html', {'air_quality_data': serializer.data})
            else:
                return render(request, 'error_template.html', {'error_message': 'Unable to fetch air quality data'})

    air_quality_form = AirQualityForm()
    return render(request, 'airquality.html', {'air_quality_form': air_quality_form})

# class WeatherDataListView(generics.ListAPIView):
#     authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access
#     serializer_class = WeatherDataSerializer
#     queryset = WeatherData.objects.all()
# weather_data_view_all = WeatherDataListView.as_view()

# class AirQualityListView(generics.ListAPIView):
#     authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access
#     serializer_class = AirQualitySerializer
#     queryset = AirQuality.objects.all()
# air_quality_view_all = AirQualityListView.as_view()

def weather_data_list(request):
    if request.method == 'POST':
        selected_records = request.POST.getlist('selected_records')
        WeatherData.objects.filter(pk__in=selected_records).delete()
    weather_data_list = WeatherData.objects.all()
    return render(request, 'weatherdata_list.html', {'weather_data_list': weather_data_list})

def air_quality_list(request):
    if request.method == 'POST':
        selected_records = request.POST.getlist('selected_records')
        AirQuality.objects.filter(pk__in=selected_records).delete()
    air_quality_list = AirQuality.objects.all()
    return render(request, 'airquality_list.html', {'air_quality_list': air_quality_list})


def weather_data_delete(request, pk):
    weather_data = get_object_or_404(WeatherData, pk=pk)
    
    if request.method == 'POST':
        weather_data.delete()
        return redirect('weather-data-list')  # Redirect to the list view after successful deletion
    
    return render(request, 'weatherdata_confirm_delete.html', {'weather_data': weather_data})

def air_quality_delete(request, pk):
    air_quality = get_object_or_404(AirQuality, pk=pk)
    
    if request.method == 'POST':
        air_quality.delete()
        return redirect('air-quality-list')  # Redirect to the list view after successful deletion
    
    return render(request, 'airquality_confirm_delete.html', {'air_quality': air_quality})
