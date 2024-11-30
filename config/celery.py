import os
import sys
import warnings
from pathlib import Path

import django
from celery import Celery


warnings.filterwarnings("ignore")


current_path = Path(__name__).parent.resolve()
sys.path.append(str(current_path / "backend"))


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
os.environ.setdefault("FLOWER_UNAUTHENTICATED_API", "true")

django.setup()

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(related_name="tasks")
