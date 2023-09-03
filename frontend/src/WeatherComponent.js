import React, { useState, useEffect } from 'react';
import axios from 'axios';

function WeatherComponent() {
  const [weatherData, setWeatherData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Fetch weather data using axios or your preferred method
    axios.get('http://localhost:8000/api/weather/nairobi')
      .then(response => {
        setWeatherData(response.data);
        setIsLoading(false); // Set loading to false once data is fetched
      })
      .catch(error => {
        console.error('Error fetching weather data:', error);
        setIsLoading(false); // Set loading to false even if there's an error
      });
  }, []);

  return (
    <div>
      {isLoading ? (
        <p>Weather data loading...</p>
      ) : weatherData ? (
        <div>
          <h2>Weather Data</h2>
          <p>City: {weatherData.city}</p>
          <p>Temperature: {weatherData.temperature}</p>
          <p>Humidity: {weatherData.humidity}</p>
          <p>Wind Speed: {weatherData.wind_speed}</p>
          <p>Condition: {weatherData.condition}</p>
        </div>
      ) : (
        <p>No weather data available.</p>
      )}
    </div>
  );
}

export default WeatherComponent;
