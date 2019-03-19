# from background_task import background
from indicator.celery import app
from indicator.models import Indicator
from datetime import datetime


@app.task
def update_indicators():
    print(datetime.now())
    indicators = Indicator.objects.all()
    print('here')
    for indicator in indicators:
        indicator.update_time_control()
        print('updated')
