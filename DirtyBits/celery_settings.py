import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DirtyBits.settings')

app = Celery('DirtyBits')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()