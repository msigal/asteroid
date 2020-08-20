from os.path import splitext
from uuid import uuid4

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.core.files.storage import FileSystemStorage
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils import timezone

from customauth.models import CustomUser


class AttachmentStorage(FileSystemStorage):
    # class to hide real binding of location to UPLOADED_FILES in migration
    def __init__(self):
        super().__init__(location=settings.UPLOADED_FILES)


attachment_storage = AttachmentStorage()


def generate_img_filename(
        instance,
        filename,
):  # pylint: disable=unused-argument
    return f'asteroid-image/{uuid4().hex}{splitext(filename)[1]}'


class Asteroid(models.Model):
    class Meta:
        verbose_name = 'Asteroid'
        verbose_name_plural = 'Asteroids'

    id = models.CharField(
        max_length=50,
        primary_key=True,
        verbose_name='ID',
    )
    name = models.CharField(
        db_index=True,
        max_length=100,
        verbose_name='Name',
    )
    nasa_jpl_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='External Url with Object image',
    )
    is_potentially_hazardous_asteroid = models.BooleanField(
        default=False,
        verbose_name='Potentially Hazaroud asteroid',
    )
    orbital_data = JSONField(
        encoder=DjangoJSONEncoder,
        blank=True,
        null=True,
        verbose_name='Object data',
    )

    def to_dict(self, fields_name=tuple()) -> dict:
        if not fields_name:
            fields_name = ('name', 'is_potentially_hazardous_asteroid', 'orbital_data')

        data = {}
        for field in fields_name:
            field_value = getattr(self, field)
            data[field] = field_value

        return data

    def __str__(self):
        return self.name


class UploadedImage(models.Model):
    class Meta:
        verbose_name = 'Uploaded image'
        verbose_name_plural = 'Uploaded images'

    user = models.ForeignKey(
        CustomUser,
        related_name='Users_images',
        on_delete=models.CASCADE,
        verbose_name='User',
    )
    image_datetime = models.DateTimeField(
        verbose_name='Date/time when image was taken',
    )
    image = models.FileField(
        upload_to=generate_img_filename,
        storage=attachment_storage,
        verbose_name='Image with asteroids captured',
        blank=True,
        null=True,
    )
    asteroids = models.ManyToManyField(
        Asteroid,
        related_name='asteroid_images',
        verbose_name='Objects, captured on image',
    )

    def __str__(self):
        return f'Image with {["#" + asteroid.name for asteroid in self.asteroids.all()]} asteroids'


class BookmarkAsteroid(models.Model):
    class Meta:
        verbose_name = 'Bookmark'
        verbose_name_plural = 'Users Bookmarks'

    user = models.ForeignKey(
        CustomUser,
        related_name='user_favorite_asteroids',
        on_delete=models.CASCADE,
        verbose_name='User',
    )
    asteroid = models.ForeignKey(
        Asteroid,
        on_delete=models.CASCADE,
        related_name='users_who_bookmarked',
        verbose_name='Asteroid',
    )

    def __str__(self):
        return f'{self.asteroid} is bookmarked for user {self.user}'
