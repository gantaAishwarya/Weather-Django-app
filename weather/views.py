from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view
import requests
import os
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils.translation import gettext as _
import demo.settings.base as config
from django.core.cache import cache
from django.utils.translation import get_language
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.decorators.cache import cache_page

def save_config(request):
    cache_duration = request.POST.get('cache_duration')
    if cache_duration:
        config.CACHE_TIMEOUT = cache_duration
    print(f'cache_timeout set to: {config.CACHE_TIMEOUT}')
    return render(request, 'config.html', {'set_val': int(int(config.CACHE_TIMEOUT) / 60)})

def configuration(request):
    return render(request, 'config.html', {'set_val': int(int(config.CACHE_TIMEOUT) / 60)})

def load_env(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

def get_api_key():
        # Reading api key from env content
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        env_file_path = os.path.join(BASE_DIR, '.env')
        load_env(env_file_path)
        API_KEY = os.getenv("API_KEY")
        return API_KEY

def get_wind_direction(wind_direction):
    if wind_direction is None:
        return None
    
    # Define wind direction ranges for each cardinal direction
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
    angle_ranges = [i * 45 for i in range(len(directions))]
    
    # Find the cardinal direction based on wind direction
    for i in range(len(directions) - 1):
        if angle_ranges[i] <= wind_direction < angle_ranges[i + 1]:
            return directions[i]
    
    # If wind direction is exactly 360 degrees, treat it as north
    if wind_direction == 360:
        return "N"
    
    return None


def get_lat_lon_from_nominatim(city):

    nominatim_api_url = f"https://nominatim.openstreetmap.org/search.php?q={city}&format=jsonv2"

    try:      
        response = requests.get(nominatim_api_url)
        response.raise_for_status()
        long_lat_data = response.json()

        if long_lat_data:
            lat = float(long_lat_data[0]['lat'])
            lon = float(long_lat_data[0]['lon'])
            return lat, lon
        else:
            return None, None
    except requests.exceptions.RequestException as e:
        print(_(f"Error fetching data from Nominatim API: {str(e)}"))
        return None, None
    
@api_view(['GET'])
def weather_view(request):
    return render(request, 'home.html')

def get_cache_timeout():
    return config.CACHE_TIMEOUT


@cache_page(get_cache_timeout())
@api_view(['GET'])
def weather_info_api(request):
    city = request.GET.get('city', None)
    current_language = get_language()
    API_KEY = get_api_key()
    cache_timeout = get_cache_timeout()

    if city:
        try:
            lat, lon = get_lat_lon_from_nominatim(city)
            #api_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}'
            api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}'
            if cache_timeout == 0 or not cache.get(city):
                #if lat is None or lon is None:
                #    return JsonResponse({'error': _('Invalid city or coordinates')}, status=400)

                response = requests.get(api_url)
                response.raise_for_status()
                weather_data = response.json()

                # Extract relevant information from the One Call API response
                current_weather_data = {
                    'city': city,
                    'current_temperature': weather_data['main']['temp'],
                    'min_temperature': weather_data['main']['temp_min'],
                    'max_temperature': weather_data['main']['temp_max'],
                    'humidity': weather_data['main']['humidity'],
                    'pressure': weather_data['main']['pressure'],
                    'wind_speed': weather_data['wind']['speed'],
                    'wind_direction': get_wind_direction(weather_data['wind']['deg']),
                    'description': weather_data['weather'][0]['description'],
                }

                if int(cache_timeout) <= 0 or not cache.get(city):
                    cache.set(city, current_weather_data, timeout=cache_timeout)
            else:
                current_weather_data = cache.get(city)

            return render(request, 'weather.html', {'current_weather': current_weather_data, 'LANGUAGE_CODE': current_language})

        except requests.exceptions.RequestException as e:
            return JsonResponse({_('error'): _(f'Error fetching weather information')}, status=500)
    else:
        return JsonResponse({_('error'): _('City is required')}, status=400)
