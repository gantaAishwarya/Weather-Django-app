from rest_framework.routers import DefaultRouter, SimpleRouter
from django.conf import settings


# make trailing slash optional for all Rest API Endpoints.
class CustomDefaultRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = "/?"