from rest_framework import serializers
from .models import CurrentWeather

class CurrentWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        # Specify the model and fields for serialization
        model = CurrentWeather
        fields = '__all__'

    def validate_current_temperature(self, value):
        # Validate the current temperature value
        if value < -50 or value > 50:
            raise serializers.ValidationError("Invalid temperature value. Temperature should be between -50 and 50 degrees Celsius.")
        return value

    def validate_wind_speed(self, value):
        # Validate the wind speed value
        if value < 0:
            raise serializers.ValidationError("Wind speed should be a positive value.")
        return value

    def validate_wind_direction(self, value):
        # Validate the wind direction value
        valid_directions = ['N', 'S', 'E', 'W']
        if value not in valid_directions:
            raise serializers.ValidationError("Invalid wind direction. Valid directions are 'N', 'S', 'E', 'W'.")
        return value
