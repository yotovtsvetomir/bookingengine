# Django imports
from django.urls import include, path
from django.conf.urls import url
from django.contrib import admin

# DRF imports
from rest_framework import routers

# Documentation imports
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Local imports
from listings import views, viewsets

schema_view = get_schema_view(
    openapi.Info(
        title="Booking API",
        default_version='v1',
        description="Booking a hotel or an apartment",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="t-yotov@yotovteam.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True
)

router = routers.DefaultRouter()
router.register(r'listings', viewsets.ListingViewSet)

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
