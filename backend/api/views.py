import requests
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import WeatherDataSerializer, AirQualitySerializer
from .models import WeatherData, AirQuality

class WeatherDataView(generics.ListAPIView):
    serializer_class = WeatherDataSerializer

    def get(self, request, city):
        api_key = '9d37bd3f822a4af6b41100758231908'
        url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}'

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Extract relevant weather data from 'data' and format the response
            weather_data = {
                'city': data['location']['name'],
                'temperature': data['current']['temp_c'],
                'humidity': data['current']['humidity'],
                'wind_speed': data['current']['wind_kph'],
                'condition': data['current']['condition']['text']
            }

            # Assuming user is properly authenticated
            weather_query = WeatherData(
                user=request.user,
                city=data['location']['name'],
                temperature=data['current']['temp_c'],
                humidity=data['current']['humidity'],
                wind_speed=data['current']['wind_kph'],
                condition=data['current']['condition']['text']
            )
            weather_query.save()

            return Response(weather_data)
        else:
            return Response({'error': 'Unable to fetch weather data'}, status=response.status_code)

weather_data_view = WeatherDataView.as_view()

class AirQualityView(generics.ListAPIView):
    serializer_class = AirQualitySerializer
    
    def get(self, request, city):
        api_key = '9d37bd3f822a4af6b41100758231908'
        air_quality_url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=1&aqi=yes'

        response = requests.get(air_quality_url)
        if response.status_code == 200:
            data = response.json()
            air_quality = data['current']['air_quality']

            air_quality_query = AirQuality(
                user=request.user,
                city=city,  # Provide the city name
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

            # Serialize the air_quality data using AirQualitySerializer
            serializer = AirQualitySerializer(air_quality_query)
            return Response(serializer.data)
        else:
            return Response({'error': 'Air quality data not available'}, status=response.status_code)

air_quality_view = AirQualityView.as_view()

class WeatherDataListView(generics.ListAPIView):
    serializer_class = WeatherDataSerializer
    queryset = WeatherData.objects.all()
weather_data_view_all = WeatherDataListView.as_view()

class AirQualityListView(generics.ListAPIView):
    serializer_class = AirQualitySerializer
    queryset = AirQuality.objects.all()
air_quality_view_all = AirQualityListView.as_view()