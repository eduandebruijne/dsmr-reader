from django.conf.urls import include
from django.urls.conf import path
from django.contrib import admin
from django.conf import settings
from rest_framework.schemas import get_schema_view


v2_api_schema = get_schema_view(
    title="DSMR-reader",
    description='REST API documentation (automatically generated).',
    version='v{}'.format(settings.DSMRREADER_VERSION),
    # Ignore default auth
    public=True,
    authentication_classes=[],
    permission_classes=[],
)

urlpatterns = [
    path('', include('dsmr_frontend.urls')),
    path('admin/', admin.site.urls),
    path('api/v2/openapi.json', v2_api_schema, name='v2-api-openapi-schema'),
    path('api/v1/', include('dsmr_api.urls.v1')),
    path('api/v2/', include('dsmr_api.urls.v2')),
]

if settings.DEBUG:
    import debug_toolbar  # pragma: no cover

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]  # pragma: no cover
