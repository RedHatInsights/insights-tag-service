from django.conf.urls import url, include
from api.views import TagViewSet, schema_view
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tags', TagViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger',
                                           cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc',
                                         cache_timeout=0), name='schema-redoc'),
]
