import os

bind = '0.0.0.0:8000'
workers = os.environ.get('WORKERS', '5')
reload = os.environ.get('GUNICORN_RELOAD', 'False')
