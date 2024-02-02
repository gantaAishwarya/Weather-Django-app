import django_filters
from .models import CurrentWeather

class CurrentWeatherFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(lookup_expr='icontains') 
    current_temperature = django_filters.NumberFilter()

    class Meta:
        model = CurrentWeather
        fields = ['city', 'current_temperature']
