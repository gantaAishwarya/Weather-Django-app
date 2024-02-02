from django.db import models
from uuid import uuid4
from django.utils.translation import gettext as _

class CurrentWeather(models.Model):
    class WindDirection(models.TextChoices):
        NORTH = 'N', _('North')
        NORTH_EAST = 'NE', _('North-East')
        EAST = 'E', _('East')
        SOUTH_EAST = 'SE', _('South-East')
        SOUTH = 'S', _('South')
        SOUTH_WEST = 'SW', _('South-West')
        WEST = 'W', _('West')
        NORTH_WEST = 'NW', _('North-West')

    # Using ID as Universal Unique Identifier
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    city = models.CharField(max_length=200, null=False, help_text=_("Name of the city"))
    current_temperature = models.FloatField(null=False, help_text=_("Current temperature in Celsius"))
    min_temperature = models.FloatField(null=True, help_text=_("Minimum temperature in Celsius"))
    max_temperature = models.FloatField(null=True, help_text=_("Maximum temperature in Celsius"))
    humidity = models.FloatField(null=True, help_text=_("Humidity percentage"))
    pressure = models.FloatField(null=True, help_text=_("Atmospheric pressure in hPa"))
    wind_speed = models.FloatField(null=True, help_text=_("Wind speed in m/s"))
    wind_direction = models.CharField(
        null=True,
        max_length=2,  # Updated to support 'NW', 'SE', etc.
        choices=WindDirection.choices,
        help_text=_("Wind direction"),
    )
    description = models.CharField(null=True, blank=True, max_length=500, help_text=_("Description"))

    class Meta:
        verbose_name_plural = _("Current Weathers")

    def __str__(self):
        return f"{self.city} - {self.current_temperature}°C"
