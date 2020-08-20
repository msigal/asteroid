from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

from django.conf import settings

from core.models import (
    Asteroid,
    BookmarkAsteroid,
    UploadedImage,
)
from customauth.models import CustomUser


def check_if_asteroid_exists(name: str) -> bool:
    return Asteroid.objects.filter(name__iexact=name).exists()


def get_asteroid_by_name(name: str) -> Asteroid:
    return Asteroid.objects.get(name=name)


def set_asteroid_bookmark_status(user: CustomUser, name: str, bookmark_add: bool = True) -> None:
    asteroid = get_asteroid_by_name(name)
    if bookmark_add:
        bookmark, _ = BookmarkAsteroid.objects.get_or_create(user=user, asteroid=asteroid)
    else:
        BookmarkAsteroid.objects.filter(
            user=user, asteroid=asteroid
        ).delete()


def get_uploaded_image_urls(user: CustomUser, asteroid_name: str) -> Optional[List[str]]:
    images_queryset = UploadedImage.objects.filter(user=user, asteroids__name__iexact=asteroid_name)
    if not images_queryset.exists():
        return
    images = [uploaded_image.image for uploaded_image in images_queryset.all()]
    result = []
    for image in images:
        result.append(
            urljoin(
                settings.BASE_SERVER_URL,
                urljoin(settings.UPLOADED_FILES_URL, image.name)
            )
        )
    return result


def get_asteroids_names() -> List[str]:
    return Asteroid.objects.all().values_list('name', flat=True)


def add_uploaded_image_data(user: CustomUser, data: Dict[str, Any]) -> UploadedImage:
    asteroid_names = data.pop('asteroids')
    asteroids = [get_asteroid_by_name(asteroid_name) for asteroid_name in asteroid_names]
    uploaded_image = UploadedImage(user=user, **data)
    uploaded_image.full_clean()
    uploaded_image.save()
    if asteroids:
        uploaded_image.asteroids.set(asteroids)
    return uploaded_image
