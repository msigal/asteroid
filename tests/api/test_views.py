import datetime

import pytest
from django.test import Client

from core.core_functions import add_uploaded_image_data


@pytest.mark.django_db
def test_signin_view__proper_call__return_token():
    client = Client()
    payload = {
        'email': 'john@foo.com',
        'password': 'example',
    }
    response = client.post(
        '/signin/',
        data=payload,
    )
    assert response.status_code == 200
    assert 'token' in response.data.keys()


@pytest.mark.django_db
def test_signin_view__unknown_user__return_error_400():
    client = Client()
    payload = {
        'username': 'unknown@foo.com',
        'password': 'example',
    }
    response = client.post(
        '/signin/',
        data=payload,
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_signup_view__proper_call__ok_created_successfully():
    client = Client()
    payload = {
        'email': 'user3@foo.com',
        'password1': 'example',
        'password2': 'example',
    }
    response = client.post(
        '/signup/',
        data=payload,
        content_type='application/json'
    )

    assert response.status_code == 201
    assert response.data['message'] == 'User user3@foo.com successfully created'


@pytest.mark.django_db
def test_signup_view__bad_request__returns_400_validation_error():
    client = Client()
    payload = {
        'email': 'user3@foo.com',
        'password1': 'example',
        'password2': 'other example',
    }
    response = client.post(
        '/signup/',
        data=payload,
        content_type='application/json'
    )

    assert response.status_code == 400
    assert response.json() == {'password1': ['password1 and password2 are not equal']}


@pytest.mark.django_db
def test_asteroid_viewset__get_by_name__no_url_images__ok_returns_dataset(user1, asteroid_1994_TA2):
    client = Client()
    client.login(email=user1.email, password='example')
    response = client.get(
        f'/asteroids/{asteroid_1994_TA2.name}/',
        content_type='application/json',
    )
    assert response.status_code == 200
    assert response.data['name'] == asteroid_1994_TA2.name
    assert response.data['image_urls'] is None


@pytest.mark.django_db
def test_asteroid_viewset__get_by_name__ok__200__returns_full_data(user1, jpg_object, jpg_object_2, asteroid_1994_TA2):
    for image in [jpg_object, jpg_object_2]:
        add_uploaded_image_data(
            user1,
            {
                'image_datetime': datetime.datetime(2020, 1, 1),
                'image': image,
                'asteroids': [asteroid_1994_TA2.name, ]
            }
        )

    client = Client()
    client.login(email=user1.email, password='example')
    response = client.get(
        f'/asteroids/{asteroid_1994_TA2.name}/',
        content_type='application/json',
    )
    assert response.status_code == 200
    assert response.data['name'] == asteroid_1994_TA2.name
    assert len(response.data['image_urls']) == 2


@pytest.mark.django_db
def test_asteroid_viewset__get_by_name__not_existing_name__returns_error_404(user1):
    client = Client()
    client.login(email=user1.email, password='example')
    response = client.get(
        f'/asteroids/NOT-FOUND/',
        content_type='application/json',
    )
    assert response.status_code == 404


@pytest.mark.django_db
def test_asteroid_viewset__set_bookmark__ok_201__bookmark_added(user1, asteroid_1994_TA2):
    client = Client()
    client.login(email=user1.email, password='example')
    response = client.post(
        f'/asteroids/{asteroid_1994_TA2.name}/bookmark/',
        content_type='application/json',
    )
    assert response.status_code == 201
    assert response.data['message'] == 'Bookmark status for asteroid (1994 TA2) successfully updated'


@pytest.mark.django_db
def test_asteroid_viewset__set_bookmark__ok_201__bookmark_removed(user1, user1_bookmark, asteroid_1994_TA2):
    client = Client()
    client.login(email=user1.email, password='example')
    response = client.post(
        f'/asteroids/{asteroid_1994_TA2.name}/bookmark/',
        data={'add_bookmark': False},
        content_type='application/json',
    )
    assert response.status_code == 201
    assert response.data['message'] == 'Bookmark status for asteroid (1994 TA2) successfully updated'


@pytest.mark.django_db
def test_asteroid_viewset__unset_bookmark__does_not_exists__ok(user1, asteroid_1994_TA2):
    client = Client()
    client.login(email=user1.email, password='example')
    response = client.post(
        f'/asteroids/{asteroid_1994_TA2.name}/bookmark/',
        data={'add_bookmark': False},
        content_type='application/json',
    )
    assert response.status_code == 201
    assert response.data['message'] == 'Bookmark status for asteroid (1994 TA2) successfully updated'


@pytest.mark.django_db
def test_upload_image_view__ok_201_image_uploaded(user1, asteroid_1994_TA2, jpg_object):
    client = Client()
    client.login(email=user1.email, password='example')
    payload = {
        "image_datetime": datetime.datetime(2020, 1, 1),
        "image": jpg_object,
        "asteroids": [asteroid_1994_TA2.name]
    }
    response = client.post(
        f'/upload-images/',
        data=payload,
    )
    assert response.status_code == 201
    assert response.data['message'] == "Image with ['#(1994 TA2)'] asteroids successfully uploaded"


@pytest.mark.django_db
def test_upload_image_view__not_existing_asteroid__returns_400_validation_error(user1, jpg_object):
    client = Client()
    client.login(email=user1.email, password='example')
    payload = {
        "image_datetime": datetime.datetime(2020, 1, 1),
        "image": jpg_object,
        "asteroids": ['NOT FOUND', ]
    }
    response = client.post(
        f'/upload-images/',
        data=payload,
    )
    assert response.status_code == 400
    assert '"NOT FOUND" is not a valid choice.' in response.data['asteroids']
