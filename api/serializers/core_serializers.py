from rest_framework import serializers

from api.utils import LazyMultipleChoiceField
from core.core_functions import get_asteroids_names
from core.models import Asteroid, UploadedImage


class AsteroidDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asteroid
        fields = ('name', 'is_potentially_hazardous_asteroid', 'orbital_data', 'image_urls')

    image_urls = serializers.ListField(
        allow_empty=True,
        allow_null=True,
        child=serializers.URLField(max_length=200, min_length=None, allow_blank=True),
        help_text='URLs for uploaded images contraing object provided',
    )


class SetBookmarkSerializer(serializers.Serializer):
    add_bookmark = serializers.BooleanField(
        default=True,
        help_text='Add/Remove from bookmarks',
    )


class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ('image_datetime', 'image', 'asteroids')

    asteroids = LazyMultipleChoiceField(
        required=True,
        allow_null=False,
        choices=get_asteroids_names,
        help_text='List of Asteroids captured on image',
    )
    image = serializers.FileField(
        allow_empty_file=False,
        help_text='Image with asteroids captured',
    )
