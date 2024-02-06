from .base import *

# https://docs.djangoproject.com/en/dev/ref/settings/#debug
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# CACHES
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        #Using in-memory caching backend for caching, 
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

#cacheing expire after 2 hours
CACHE_TTL = 60 * 60 * 2



ADMIN_URL = "admin/"