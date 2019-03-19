# http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simulator.settings')

app = Celery('indicator')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.conf.timezone = 'Asia/Tehran'

# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
app.conf.beat_schedule = {
    'update_indicators': {
        'task': 'indicator.tasks.update_indicators',
        'schedule': crontab(minute=14, hour=4),
    },
}
