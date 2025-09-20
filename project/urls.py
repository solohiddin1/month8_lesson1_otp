from django.contrib import admin
from django.urls import path,include
# from app import urls
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(title="My API", default_version='v1'),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('app.urls')),
    path('swagger/',schema_view.with_ui('swagger',cache_timeout=0),name='swagger-schema'),
]
