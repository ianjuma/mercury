import os


BROKER_TRANSPORT_OPTIONS = os.environ.get('BROKER_TRANSPORT_OPTIONS')
CELERY_RESULT_BACKEND    = os.environ.get('CELERY_RESULT_BACKEND')

BROKER_URL = os.environ.get('BROKER_URL')
APIKEY     = os.environ.get('APIKEY')
