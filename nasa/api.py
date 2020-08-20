from typing import Any, Dict, Optional

import requests
from django.conf import settings

from nasa.exceptions import NasaApiError


def get_asteroid_data_from_nasa() -> Optional[Dict[str, Any]]:
    """
    Proxy View for Nasa API
    Browses the overall Asteroid data-set
    """
    response = requests.get(
        url=settings.NASA_URL_ASTEROIDS,
        params={
            'api_key': settings.NASA_API_KEY,
            'page': 1,
        }
    )
    if response.status_code != 200:
        error = response.json()['error']
        raise NasaApiError(error)

    data = response.json()
    return data.get('near_earth_objects')
