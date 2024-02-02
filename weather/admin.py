from django.contrib import admin
from .models import CurrentWeather

#show models in django admin panel
class WeatherAdmin(admin.ModelAdmin):
    search_fields = ["city"]
    list_display = ["city"]

admin.site.register(CurrentWeather)
