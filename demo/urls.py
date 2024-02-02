from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, re_path
from weather.views import weather_info_api 

# Swagger documentation setup
schema_view = get_schema_view(
    openapi.Info(
        title="CheMondis API",
        default_version='v1',
        description="CheMondis Demo Documentation",
        terms_of_service="#",
        contact=openapi.Contact(email="contact@cheMondis.net"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('api/weather', weather_info_api, name='weather-info'),  # Use the function-based view directly
    re_path(r'^docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# URL pattern for serving static files collected during python manage.py collectstatic for efficient debugging
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "CheMondis Super Admin"
admin.site.site_title = "CheMondis"
admin.site.index_title = "CheMondis Super Admin"
