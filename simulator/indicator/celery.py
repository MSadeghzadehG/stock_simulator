# http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simulator.settings')

app = Celery('indicator')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'Asia/Tehran'

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update_indicators': {
        'task': 'indicator.tasks.update_indicators',
        'schedule': crontab(hour=12, minute=0),
    },
    'update_records': {
        'task': 'indicator.tasks.update_records',
        'schedule': crontab(hour=17, minute=0),
    },
    'update_today': {
        'task': 'indicator.tasks.update_today',
        'schedule': crontab(hour=11, minute=30),
    },
}
