import os
import logging

from celery import Celery
from celery.signals import setup_logging
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")


@setup_logging.connect
def config_loggers(*args, **kwags):
    from logging.config import dictConfig
    from django.conf import settings

    dictConfig(settings.LOGGING)


app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     "sample_task": {
#         "task": "sample_task",
#         "schedule": crontab(minute="*/1"),
#     },
#     "db_task": {
#         "task": "get_avg",
#         "schedule": crontab(minute="*/1"),
#     },
# }
