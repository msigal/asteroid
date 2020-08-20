import os
from unittest.mock import MagicMock

import pytest

from nasa.api import get_asteroid_data_from_nasa
from nasa.exceptions import NasaApiError
from tests.nasa.utils import mock_data

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')


def test_get_asteroid_data_from_nasa__200_ok(mocker):
    expected_data = mock_data(os.path.join(DATA_DIR, f'mock_response_200_ok.json'))
    mocker.patch(
        'nasa.api.requests.get',
        return_value=MagicMock(
            status_code=200,
            content=expected_data,
        )
    )
    get_asteroid_data_from_nasa()


def test_get_asteroid_data_from_nasa__invalid_api_key__return_403(mocker):
    expected_data = mock_data(os.path.join(DATA_DIR, f'mock_response_403.json'))
    mocker.patch(
        'nasa.api.requests.get',
        return_value=MagicMock(
            status_code=403,
            content=expected_data,
        )
    )
    with pytest.raises(NasaApiError):
        get_asteroid_data_from_nasa()
