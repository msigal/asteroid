import datetime
from urllib.parse import urljoin

import pytest
from django.conf import settings

from core.core_functions import (
    check_if_asteroid_exists,
    get_asteroid_by_name,
    set_asteroid_bookmark_status,
    get_asteroids_names,
    get_uploaded_image_urls,
    add_uploaded_image_data,

)
from core.models import BookmarkAsteroid, UploadedImage


@pytest.mark.django_db
@pytest.mark.parametrize(
    'asteroid_name, found',
    [('(1995 SC1)', True), ('Not existing name', False)]
)
def test_check_if_asteroid_exists__ok(asteroid_name, found):
    assert check_if_asteroid_exists(asteroid_name) is found


@pytest.mark.django_db
def test_get_asteroid_by_name(asteroid_1995_SC1):
    assert get_asteroid_by_name(asteroid_1995_SC1) == asteroid_1995_SC1


@pytest.mark.django_db
def test_set_asteroid_bookmark_status__true__created(asteroid_1994_TA2, asteroid_1995_SC1, user1):
    set_asteroid_bookmark_status(user1, asteroid_1995_SC1.name, True)
    set_asteroid_bookmark_status(user1, asteroid_1994_TA2.name, True)
    bookmarks = {bookmark.asteroid for bookmark in BookmarkAsteroid.objects.filter(user=user1)}
    assert len(bookmarks) == 2
    assert bookmarks == {asteroid_1995_SC1, asteroid_1994_TA2}


@pytest.mark.django_db
def test_set_asteroid_bookmark_status__false__deleted(asteroid_1994_TA2, user1):
    set_asteroid_bookmark_status(user1, asteroid_1994_TA2.name)
    set_asteroid_bookmark_status(user1, asteroid_1994_TA2.name, False)
    bookmarks = BookmarkAsteroid.objects.filter(user=user1).exists()
    assert bookmarks is False


@pytest.mark.django_db
def get_asteroids_names():
    assert len(get_asteroids_names()) == 20


@pytest.mark.django_db
def test_add_uploaded_image_data__successfully_added(user1, jpg_object, asteroid_1994_TA2, asteroid_1995_SC1):
    data = {
        'image_datetime': datetime.datetime(2020, 1, 1),
        'image': jpg_object,
        'asteroids': [asteroid_1994_TA2.name, asteroid_1995_SC1.name]
    }

    uploaded_image = add_uploaded_image_data(user1, data)
    uploaded_image.image.open(mode="rb")
    executed = uploaded_image.image.read()
    uploaded_image.image.close()
    jpg_object.seek(0)
    assert executed == jpg_object.read()
    assert set(uploaded_image.asteroids.all()) == {asteroid_1995_SC1, asteroid_1994_TA2}


@pytest.mark.django_db
def test_get_uploaded_image_urls(user1, jpg_object, jpg_object_2, asteroid_1994_TA2):
    for image in [jpg_object, jpg_object_2]:
        add_uploaded_image_data(
            user1,
            {
                'image_datetime': datetime.datetime(2020, 1, 1),
                'image': image,
                'asteroids': [asteroid_1994_TA2.name, ]
            }
        )
    executed = get_uploaded_image_urls(user1, asteroid_1994_TA2.name)
    expected = [
        urljoin(settings.BASE_SERVER_URL,
                urljoin(settings.UPLOADED_FILES_URL, image))
        for image in UploadedImage.objects.filter(user=user1).values_list('image', flat=True)
    ]
    assert executed == expected


@pytest.mark.django_db
def test_get_uploaded_image_urls__other_user__return_None(user1, user2, jpg_object, jpg_object_2, asteroid_1994_TA2):
    for image in [jpg_object, jpg_object_2]:
        add_uploaded_image_data(
            user1,
            {
                'image_datetime': datetime.datetime(2020, 1, 1),
                'image': image,
                'asteroids': [asteroid_1994_TA2.name, ]
            }
        )
    executed = get_uploaded_image_urls(user2, asteroid_1994_TA2.name)
    assert executed is None
