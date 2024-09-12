import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
os.environ.setdefault("FLOWER_UNAUTHENTICATED_API", "true")

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(related_name="tasks")
