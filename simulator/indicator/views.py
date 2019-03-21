from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from indicator.models import Stock, Record, Indicator, Bought_stock
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.template import loader
from django.utils import timezone
from datetime import datetime, date
from django import forms
import requests
from . import tasks
#from background_task import background


class IndicatorForm(forms.Form):

    name = forms.CharField(max_length=100)
    algorithm = forms.CharField(max_length=200)
    start_date = forms.DateField(
        input_formats=['%m/%d/%Y'],
        widget=forms.DateInput(attrs={
            'class': 'datepicker'
        })
    )
    end_date = forms.DateField(
        input_formats=['%m/%d/%Y'],
        widget=forms.DateInput(attrs={
            'class': 'datepicker'
        })
    )
    update_daily = forms.BooleanField(required=False)

    # def clean(self):


def home(request):
    form = IndicatorForm(auto_id=False)
    # tasks.update_records.delay()
    template = loader.get_template('indicator/home.html')
    context = {'form': form}
    return HttpResponse(template.render(context, request))



def update_request(request):
    tasks.update_records.delay()
    return redirect('/stocks')



def stocks_table(request):
    from django.db.models import IntegerField
    from django.db.models.functions import Cast
    template = loader.get_template('indicator/stocks.html')
    stocks = Stock.objects.annotate(
        my_integer_field=Cast(
            'hajm_moamelat', IntegerField())
            ).order_by('my_integer_field', 'hajm_moamelat').reverse()
    context = {
        'stocks': serializers.serialize("python", stocks),
        'headers': [field.name for field in Stock._meta.get_fields()][3:]
        }
    return HttpResponse(template.render(context, request))


def records_table(request, id):
    template = loader.get_template('indicator/records.html')
    stock = Stock.objects.get(tmc_id=id)
    records = Record.objects.filter(stock=stock).order_by('date').reverse()
    context = {
        'records': serializers.serialize("python", records),
        'headers': [field.name for field in Record._meta.get_fields()][1:]
        }
    return HttpResponse(template.render(context, request))


def boughts_table(request, name):
    template = loader.get_template('indicator/bought.html')
    indicator = Indicator.objects.get(name=name)
    # indicator.update_profit()
    boughts = indicator.trade_log.all().order_by('profit').reverse()
    context = {
        'stocks': serializers.serialize("python", boughts),
        'headers': [field.name for field in Bought_stock._meta.get_fields()][3:]
        }
    return HttpResponse(template.render(context, request))


def indicators_table(request):
    template = loader.get_template('indicator/indicators.html')
    context = {
        'headers': [field.name for field in Indicator._meta.get_fields()][1:-2]
        }
    return HttpResponse(template.render(context, request))


def add_indicator(request):
    # if this is a POST request we need to process the form data
    # create a form instance and populate it with data from the request:
    form = IndicatorForm(request.POST)
    # check whether it's valid:
    if form.is_valid():
        start_time = Indicator.add_time_to_date(form.cleaned_data['start_date'])
        end_time = Indicator.add_time_to_date(form.cleaned_data['end_date'])
        new_indicator = Indicator(
            name=form.cleaned_data['name'],
            algorithm=form.cleaned_data['algorithm'],
            start_time=start_time,
            end_time=end_time
            )
        if form.cleaned_data['update_daily']:
            new_indicator.end_time = None
        new_indicator.save()
    else:
        print('invalid form')
        return redirect('/')
    return redirect('/indicators')


def delete_indicator(request, name):
    indicator = Indicator.objects.all().get(name=name)
    # print(indicator)
    indicator.mydelete()
    print(len(Indicator.objects.all()))
    print(len(Bought_stock.objects.all()))
    return redirect('/indicators')


def update_indicator(request, name):
    indicator = Indicator.objects.all().get(name=name)
    indicator.update_time_indicator()
    return redirect('/indicators')


def delete_database(request):
    # Record.objects.all().delete()
    # Stock.objects.all().delete()
    # Indicator.objects.all().delete()
    for o in Indicator.objects.all():
        o.mydelete()
    print(len(Bought_stock.objects.all()))
    # print(len(Record.objects.all()))
    # Record.objects.filter(date=20190308).delete()
    # print(len(Record.objects.all()))
    return HttpResponse('deleted')


def get_indicator(request):
    indicator_names = Indicator.objects.all().values_list('name', flat=True)
    indicators = {}
    for name in indicator_names:
        obj = []
        for indicator_field in Indicator._meta.get_fields():
            if indicator_field.name not in ('bought', 'id', 'trade_log'):
                obj.append(Indicator.objects.values_list(
                    indicator_field.name, flat=True).get(name=name))
        indicators[name] = obj
    return JsonResponse(indicators)


def update_stocks_today():
    r = requests.get('http://www.tsetmc.com/tsev2/data/MarketWatchInit.aspx?h=0&r=0')
    # headers = ['id','?','namad','nam','?','avalin','payani','akharin moamele','tedad moamelat','hajm moamelat','arzesh mamelat','baze rooz kam','baze rooz ziad','dirooz','eps','?','?','?','?','mojaz ziad','mojaz kam','?','?']
    # print(len(r.text.split('@')[2].split(';')))
    # print(len(Record.objects.all()))
    print(len(Stock.objects.all()))
    stocks_list = r.text.split('@')[2].split(';')
    # print(stocks_list)
    today = Indicator.datetime_to_dateint(datetime.now())
    for i in stocks_list:
        # print(i.split(',')[:23])
        seprated = i.split(',')[:23]
        # print(seprated)
        # sleep(1)
        new_entry = Stock(seprated[0], *seprated)
        try:
            found = Stock.objects.get(tmc_id=seprated[0])
            found.update(*seprated[1:])
            # found.save(id=seprated[0])
            print('found'+str(found))
            found.save()
        except ObjectDoesNotExist:
            print('new'+str(new_entry))
            new_entry.save()
        # try:
        #     found = Record.objects.get(stock=i,date = today)
        # except:
        #     new_record = Record(stock=stock,date=today,first=stock.avalin,high=stock.baze_rooz_ziad,low=stock.baze_rooz_kam,close=stock.payani,\
        #             value=stock.arzesh_moamelat,vol=stock.hajm_moamelat,openint=stock.tedad_moamelat,per='D',openp=stock.dirooz,last=stock.akharin_moamele)
        #     print('new',new_record,)
        #     new_record.save()
    print(len(Stock.objects.all()))
    # print([field.name for field in Stock._meta.get_fields()])


def update_stock_history(stock):
    get_data_url = 'http://tsetmc.ir/tsev2/data/Export-txt.aspx?t=i&a=1&b=0&i='
    get_data_url2 = 'http://members.tsetmc.com/tsev2/data/InstTradeHistory.aspx?i='
    get_data_url3 = '&Top=999999&A=0'
    check = False
    r = requests.get(get_data_url+stock.getID())
    while r.status_code == 500:
        if check:
            # r = requests.get(get_data_url2+stock.getID()+get_data_url3)
            r = requests.get(get_data_url+stock.getID())
            check = False
        else:
            r = requests.get(get_data_url+stock.getID())
            check = True
    # print(r.text)
    rr = r.text.split('\r\n')
    # print(rr)
    if len(rr) > 0:
        del rr[-1]
    if len(rr) > 0:
        del rr[0]
    # print(rr)
    for j in rr:
        seprated = j.split(',')
        # print(seprated[1])
        try:
            found = Record.objects.get(stock=stock, date=seprated[1])
            print('found'+str(found))
            # for attr, value in found.__dict__.items():
            #     print(attr, value)
            break     # CHECKOUT THIS SHOULD BE COMMENT OR NOT!!
        except ObjectDoesNotExist:
            new_entry = Record.create(stock, *seprated)
            new_entry.save()
            print('new'+str(new_entry))
    # print(len(Record.objects.all()))
    # headers = ['Ticker','date','first','high','low','close','value','vol','openint','per','open','last']
    # print([field.name for field in Record._meta.get_fields()])


def update():
    update_stocks_today()
    all_stock = Stock.objects.all()
    for i in all_stock:
        update_stock_history(i)
        print(list(all_stock).index(i))

