from typing import Dict, List

from django.core.management import BaseCommand

from core.models import Asteroid
from nasa.api import get_asteroid_data_from_nasa


class Command(BaseCommand):
    help = 'Load Data on asteroids into internal models'

    @staticmethod
    def _get_objects(model_cls, received_data: List[Dict]):
        result = []
        meta_fields = [field.name for field in model_cls._meta.fields]
        for item in received_data:
            result.append(model_cls(**{field: item.get(field) for field in meta_fields}))
        return result

    def handle(self, *args, **options):
        received_data = get_asteroid_data_from_nasa()
        if not received_data:
            print('No data received')
        objs = self._get_objects(Asteroid, received_data)
        Asteroid.objects.bulk_create(objs, ignore_conflicts=True)
