# from background_task import background
from indicator.celery import app
from indicator.models import Indicator, Stock, Record
from datetime import datetime
# from indicator.views import update
from . import views


@app.task
def update_indicators():
    print(datetime.now())
    indicators = Indicator.objects.all()
    print('here')
    for indicator in indicators:
        indicator.update_time_control()
        print('updated')


@app.task
def update_records():
    Record.objects.filter(Ticker='').delete()
    print('day records deleted', Record.objects.filter(Ticker=''))
    views.update()


@app.task
def update_today():
    views.update_stocks_today()
    stocks = Stock.objects.all()
    today = Indicator.datetime_to_dateint(datetime.now())
    for stock in stocks:
        new_record = Record(
            stock=stock,
            date=today,
            first=stock.avalin,
            high=stock.baze_rooz_ziad,
            low=stock.baze_rooz_kam,
            close=stock.payani,
            value=stock.arzesh_moamelat,
            vol=stock.hajm_moamelat,
            openint=stock.tedad_moamelat,
            per='D',
            openp=stock.dirooz,
            last=stock.akharin_moamele
            )
        print('new', new_record, today)
        new_record.save()
