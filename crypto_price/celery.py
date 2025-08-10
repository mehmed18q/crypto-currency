import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crypto_price.settings')

app = Celery('crypto_price')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
