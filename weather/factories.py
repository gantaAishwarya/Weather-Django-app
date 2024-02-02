import factory
from factory.django import DjangoModelFactory
from .models import CurrentWeather

class CurrentWeatherFactory(DjangoModelFactory):
    class Meta:
        model = CurrentWeather

    city = factory.Faker('city')
    current_temperature = factory.Faker('pyfloat', positive=True)
    min_temperature = factory.Faker('pyfloat', positive=True)
    max_temperature = factory.Faker('pyfloat', positive=True)
    humidity = factory.Faker('pyfloat', positive=True, max_value=100)
    pressure = factory.Faker('pyfloat', positive=True)
    wind_speed = factory.Faker('pyfloat', positive=True)
    wind_direction = factory.Faker('random_element', elements=['N', 'S', 'E', 'W'])
    description = factory.Faker('text', max_nb_chars=500)
