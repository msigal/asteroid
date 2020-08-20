import os

import pytest
from django.core.management import call_command

from core.models import Asteroid
from tests.nasa.utils import mock_data

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')


@pytest.mark.django_db
def test_loadnasa__records_successfully_created(mocker):
    Asteroid.objects.all().delete()
    expected_data = mock_data(os.path.join(DATA_DIR, f'mock_response_200_ok.json'))
    mocker.patch(
        'nasa.api.get_asteroid_data_from_nasa',
        return_value=expected_data
    )

    call_command('loadnasa')
    executed_data = Asteroid.objects.count()
    assert executed_data == len(expected_data)


@pytest.mark.django_db
def test_loadnasa__multiple_apply__doesnt_create_duplicated_records(mocker):
    Asteroid.objects.all().delete()
    expected_data = mock_data(os.path.join(DATA_DIR, f'mock_response_200_ok.json'))
    mocker.patch(
        'nasa.api.get_asteroid_data_from_nasa',
        return_value=expected_data
    )

    call_command('loadnasa')
    call_command('loadnasa')
    call_command('loadnasa')
    call_command('loadnasa')

    executed_data = Asteroid.objects.count()
    assert executed_data == len(expected_data)
