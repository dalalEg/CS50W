# movie_theater/celery.py
import os
import django
from celery import Celery

# 1) point at your settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_theater.settings')

# 2) let Django bootstrap its apps before we import any models/tasks
django.setup()

# 3) create the Celery app
app = Celery('movie_theater')
app.config_from_object('django.conf:settings', namespace='CELERY')

# 4) have Celery auto‐discover all tasks.py in INSTALLED_APPS
app.autodiscover_tasks()
