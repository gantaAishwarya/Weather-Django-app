import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')

#application object interfaces with web servers to handle http requests
application = get_wsgi_application()