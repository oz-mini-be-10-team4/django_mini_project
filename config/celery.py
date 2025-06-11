import os

from celery import Celery

# settings 경로 명시
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")

app = Celery("django_mini_project")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
