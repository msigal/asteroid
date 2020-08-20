import psycopg2
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.db import connections
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from rest_framework.authtoken.models import Token

from core.models import Asteroid, BookmarkAsteroid
from customauth.models import CustomUser


def run_sql(sql):
    from django.conf import settings

    db_conf = settings.DATABASES['default']
    conn = psycopg2.connect(
        host=db_conf['HOST'],
        port=db_conf['PORT'],
        user=db_conf['USER'],
        password=db_conf['PASSWORD'],
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql)
    conn.close()


@pytest.yield_fixture(scope='session')
def django_db_setup(django_db_blocker):
    """
    Creating a test database and apply migrations to initialize tables.
    """
    from django.conf import settings

    origin_db_name = settings.DATABASES['default']['NAME']

    test_db_name = 'test_' + origin_db_name
    settings.DATABASES['default']['NAME'] = test_db_name

    run_sql(f'DROP DATABASE IF EXISTS {test_db_name}')
    run_sql(f'CREATE DATABASE {test_db_name}')

    with django_db_blocker.unblock():
        call_command('migrate')

    yield

    for connection in connections.all():
        connection.close()

    # Comment the line to explore post-test data
    run_sql(f'DROP DATABASE {test_db_name}')


@pytest.fixture(scope="session", autouse=True)
def load_fixtures(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loadnasa')
        call_command(
            'loaddata',
            'test_accounts.json',
        )


@pytest.fixture
def user1():
    return CustomUser.objects.get(pk=1)


@pytest.fixture
def user2():
    return CustomUser.objects.get(pk=2)


@pytest.fixture
def asteroid_1994_TA2():
    return Asteroid.objects.get(id=3092128)


@pytest.fixture
def asteroid_1995_SC1():
    return Asteroid.objects.get(id=3092141)


@pytest.fixture
def jpg_object():
    return SimpleUploadedFile(
        name='test.jpg',
        content=bytes.fromhex('FF D8 FF FF'),
        content_type='image/jpeg'
    )


@pytest.fixture
def jpg_object_2():
    return SimpleUploadedFile(
        name='test.jpg',
        content=bytes.fromhex('FF D8 FF FF'),
        content_type='image/jpeg'
    )


@pytest.fixture
def user1_token():
    return Token.objects.create(user=CustomUser.objects.get(pk=1))


@pytest.fixture
def user1_bookmark():
    return BookmarkAsteroid.objects.create(
        user=CustomUser.objects.get(pk=1),
        asteroid=Asteroid.objects.get(id=3092141)
    )

