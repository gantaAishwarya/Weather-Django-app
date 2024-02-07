import django_filters
from .models import CurrentWeather

# Define a filter for the CurrentWeather model
class CurrentWeatherFilter(django_filters.FilterSet):
    # Filter for 'city' field with case-insensitive partial matching
    city = django_filters.CharFilter(lookup_expr='icontains') 
    # Filter for 'current_temperature' field with exact matching
    current_temperature = django_filters.NumberFilter()

    class Meta:
        # Specify the model for which the filter is created
        model = CurrentWeather
        # Specify the fields to be used for filtering
        fields = ['city', 'current_temperature']