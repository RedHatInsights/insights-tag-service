# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from api.models import Tag
from api.serializers import TagSerializer
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import viewsets
from rest_framework.permissions import AllowAny


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


schema_view = get_schema_view(
    openapi.Info(
        title="Insights Platform Tag API",
        default_version='v1',
        description="A REST API to manage tags in the Insights Platform.",
    ),
    validators=['flex'],
    public=True,
    permission_classes=(AllowAny,),
)
