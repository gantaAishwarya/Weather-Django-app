import os
import environ
from corsheaders.defaults import default_headers
from pathlib import Path
from django.utils.translation import gettext as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
#BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = environ.Path(__file__) - 3


#Reading env content
env = environ.Env()
env.read_env(".env")

API_KEY = env.str("API_KEY", default='51c5936af0023fb3c9cd87d344b08b22')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'django-insecure-apwml5t&y%p9k-y(m(qq3i45sqpp=&8v$18#8=hq--ox#26oml'
SECRET_KEY = env.str("SECRET_KEY", default='django-insecure-36_4n+f^f$#goaw7j1la^13i32n&7l+=1gc3ak851%tqv1@jzd')

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])
#ALLOWED_HOSTS = []


# Application definition

DJANGO_APPS  = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'mathfilters',
    "rest_framework.authtoken",
    "corsheaders",
    "django_extensions",
    "django_filters",
    'coreapi',
    'drf_yasg',
    'debug_toolbar'
]

LOCAL_APPS = [
    "weather.apps.CurrentWeatherConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]


ROOT_URLCONF = 'demo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'demo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

#Default cache timeout
CACHE_TIMEOUT = 300 

REDIS_HOST = os.environ.get('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379:1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


if env.str("ENVIRONMENT", default="production") == "local":
    DATABASES = {
    "default": env.db("DATABASE_URL", default="postgres:///ch_demo_db")
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env.str("DJANGO_DATABASE_NAME"),
            "USER": env.str("DJANGO_DATABASE_USER"),
            "PASSWORD": env.str("DJANGO_DATABASE_PASSWORD"),
            "HOST": env.str("DJANGO_DATABASE_HOST"),
            "PORT": env.str("DJANGO_DATABASE_PORT", default=5432),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/



# Set the default language

LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('en-us', 'English'),
    ('fr', 'French'),
    ('es', 'Spanish'),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

SITE_ID = 1



LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

STATIC_ROOT = str(BASE_DIR.path("staticfiles"))
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    str(BASE_DIR.path("static")),
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# CORS SETTINGS
CORS_ALLOW_HEADERS = list(default_headers) + [
    "ch-header", # Foodtracker custom header
    "baggage", # for sentry configuration
    "sentry-trace", # for sentry configuration
]

CORS_ORIGIN_ALLOW_ALL = env.bool("CORS_ORIGIN_ALLOW_ALL", default=True)
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = env.list("CORS_ORIGIN_WHITELIST", default=[])

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Rest Framework Settings =============
PAGE_SIZE = env("PAGE_SIZE", default=50)
REST_FRAMEWORK = {
    # if not specified otherwise, anyone can access a view (this is the default)
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
        #"rest_framework.permissions.IsAuthenticated",
    ),
    # if required, which authentication is eligible?
    "DEFAULT_AUTHENTICATION_CLASSES": (
        #"rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
    # input formats the API can handle
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    #  output format supported by the API
    "DEFAULT_RENDERER_CLASSES": (
        'rest_framework.renderers.JSONRenderer',
        #"rest_framework.renderers.BrowsableAPIRenderer",
    ),
    # throttling of requests
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {"anon": "2/second"},
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "TEST_REQUEST_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": PAGE_SIZE,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}

