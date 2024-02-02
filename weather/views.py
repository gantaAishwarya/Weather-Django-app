from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view
import requests
import os

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
    
    return None  # Invalid wind direction


@api_view(['GET'])
@cache_page(60 * 5)  # Cache for 5 minutes
def weather_info_api(request):

    city = request.query_params.get('city', None)
        
    if city:
        city = city.lower()
        #lat = get_latitude(city)
        #lon = get_longitude(city)
        lat = request.query_params.get('lat', None)
        lon = request.query_params.get('lon', None)

        if lat is None or lon is None:
            return JsonResponse({'error': 'Invalid city or coordinates'}, status=400)

        API_KEY = get_api_key()
        api_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}'
        

        try:
            response = requests.get(api_url)
            response.raise_for_status()
            weather_data = response.json()

            # Extract relevant information from the One Call API response
            current_weather_data = {
                'city': city,  # 'Zocca' in the provided response
                'current_temperature': weather_data['main']['temp'],
                'min_temperature': weather_data['main']['temp_min'],
                'max_temperature': weather_data['main']['temp_max'],
                'humidity': weather_data['main']['humidity'],
                'pressure': weather_data['main']['pressure'],
                'wind_speed': weather_data['wind']['speed'],
                'wind_direction': get_wind_direction(weather_data['wind']['deg']),
                'description': weather_data['weather'][0]['description'],
            }


            return JsonResponse(current_weather_data, status=200)

        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': f'Error fetching weather information: {str(e)}'}, status=500)


    else:
        return JsonResponse({'error': 'City is required'}, status=400)


    
   