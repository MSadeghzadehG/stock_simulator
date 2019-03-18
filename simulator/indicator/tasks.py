from background_task import background
from indicator.models import Indicator


@background(schedule=0)
def update_indicators():
    indicators = Indicator.objects.all()
    # print('here')
    for indicator in indicators:
        indicator.update_control(
            Indicator.datetime_to_dateint(indicator.start_time),
            Indicator.datetime_to_dateint(indicator.end_time)
        )
        print('updated')
