# movie_theater/celery.py
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie_theater.settings")

app = Celery("movie_theater")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
