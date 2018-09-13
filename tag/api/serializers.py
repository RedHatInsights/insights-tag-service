from rest_framework import serializers
from api.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('created_at', 'updated_at', 'id', 'name', 'description')
