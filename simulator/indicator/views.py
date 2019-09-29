from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from indicator.models import Stock, Indicator
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.template import loader
from django.utils import timezone
from datetime import datetime, date
from django import forms
import requests
from . import tasks
from rest_framework import viewsets
from . import tmc_utils

# from indicator.serializers import StockSerializer

# class StockViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows stocks to be viewed or edited.
#     """
#     queryset = Stock.objects.all().order_by('nam')
#     serializer_class = StockSerializer


class IndicatorForm(forms.Form):

    name = forms.CharField(max_length=100)
    # algorithm = forms.CharField(max_length=200)
    algorithm_name = forms.ChoiceField(
        choices=[
            (i.split("_")[1], i.split("_")[1])
            for i in dir(Indicator)
            if i.startswith("algo_")
        ]
    )
    algorithm_inputs = forms.CharField(max_length=100)
    start_date = forms.DateField(
        input_formats=["%m/%d/%Y"],
        widget=forms.DateInput(attrs={"class": "datepicker"}),
    )
    end_date = forms.DateField(
        input_formats=["%m/%d/%Y"],
        widget=forms.DateInput(attrs={"class": "datepicker"}),
    )
    update_daily = forms.BooleanField(required=False)

    def clean_algorithm_inputs(self):
        data = self.cleaned_data["algorithm_inputs"]
        try:
            print(list(map(int, data.split(","))))
        except:
            raise forms.ValidationError("choose like this: 3,5,7")
        return data


def home(request):
    update_stocks_today()
    form = IndicatorForm(auto_id=False)
    # tasks.update_records.delay()
    template = loader.get_template("indicator/home.html")
    context = {"form": form}
    return HttpResponse(template.render(context, request))


# def update_request(request):
#     tasks.update_records.delay()
#     return redirect('/stocks')


# def stocks_table(request):
#     from django.db.models import IntegerField
#     from django.db.models.functions import Cast
#     template = loader.get_template('indicator/stocks.html')
#     stocks = Stock.objects.annotate(
#         my_integer_field=Cast(
#             'hajm_moamelat', IntegerField())
#             ).order_by('my_integer_field', 'hajm_moamelat').reverse()
#     stocks = serializers.serialize("python", stocks)
#     # print(stocks)
#     context = {
#         'stocks': stocks,
#         'headers': [field.name for field in Stock._meta.get_fields()][2:]
#         }
#     return HttpResponse(template.render(context, request))


# def records_table(request, id):
#     template = loader.get_template('indicator/records.html')
#     stock = Stock.objects.get(tmc_id=id)
#     records = Record.objects.filter(stock=stock).order_by('date').reverse()
#     context = {
#         'records': serializers.serialize("python", records),
#         'headers': [field.name for field in Record._meta.get_fields()][1:]
#         }
#     return HttpResponse(template.render(context, request))


# def boughts_table(request, name):
#     template = loader.get_template('indicator/bought.html')
#     indicator = Indicator.objects.get(name=name)
#     # indicator.update_profit()
#     boughts = indicator.trade_log.all().order_by('profit').reverse()
#     context = {
#         'stocks': serializers.serialize("python", boughts),
#         'headers': [field.name for field in Bought_stock._meta.get_fields()][3:]
#         }
#     return HttpResponse(template.render(context, request))


# def indicators_table(request):
#     template = loader.get_template('indicator/indicators.html')
#     context = {
#         'headers': [field.name for field in Indicator._meta.get_fields()][1:-2]
#         }
#     return HttpResponse(template.render(context, request))


# def add_indicator(request):
#     # if this is a POST request we need to process the form data
#     # create a form instance and populate it with data from the request:
#     form = IndicatorForm(request.POST)
#     # check whether it's valid:
#     if form.is_valid():
#         print(form.cleaned_data['algorithm_name'])
#         print(form.cleaned_data['algorithm_inputs'])
#         start_time = Indicator.add_time_to_date(form.cleaned_data['start_date'])
#         end_time = Indicator.add_time_to_date(form.cleaned_data['end_date'])
#         algorithm = str(form.cleaned_data['algorithm_name']) + '([' + str(form.cleaned_data['algorithm_inputs']) + '])'
#         new_indicator = Indicator(
#             name=form.cleaned_data['name'],
#             algorithm=algorithm,
#             start_time=start_time,
#             end_time=end_time
#             )
#         if form.cleaned_data['update_daily']:
#             new_indicator.end_time = None
#         new_indicator.save()
#     else:
#         print('invalid form')
#         return redirect('/')
#     return redirect('/indicators')


# def delete_indicator(request, name):
#     print('deleting boughts of',name,'...')
#     indicator = Indicator.objects.all().get(name=name)
#     indicator.mydelete()
#     # print(len(Indicator.objects.all()))
#     # print(len(Bought_stock.objects.all()))
#     return redirect('/indicators')


# def update_indicator(request, name):
#     print(name, 'update started')
#     tasks.update_indicator.delay(name)
#     return redirect('/indicators')


# def delete_database(request):
#     Record.objects.all().delete()
#     # Stock.objects.all().delete()
#     # Indicator.objects.all().delete()
#     # for o in Indicator.objects.all():
#     #     o.mydelete()
#     # print(len(Bought_stock.objects.all()))
#     # print(len(Record.objects.all()))
#     # Record.objects.filter().delete()
#     # print(len(Record.objects.all()))
#     return HttpResponse('deleted')


# def get_indicator(request):
#     indicator_names = Indicator.objects.all().values_list('name', flat=True)
#     indicators = {}
#     for name in indicator_names:
#         obj = []
#         for indicator_field in Indicator._meta.get_fields():
#             if indicator_field.name not in ('bought', 'id', 'trade_log'):
#                 obj.append(Indicator.objects.values_list(
#                     indicator_field.name, flat=True).get(name=name))
#         indicators[name] = obj
#     return JsonResponse(indicators)


# def get_stocks(request):
#     stock_names = Stock.objects.all().values_list('tmc_id', flat=True)
#     stocks = {}
#     for tmc_id in stock_names:
#         obj = []
#         for stock_field in Stock._meta.get_fields():
#             if stock_field.name not in ('record', 'bought_stock'):
#                 # print(tmc_id, stock_field)
#                 # print(Stock.objects.filter(tmc_id=tmc_id).values_list(stock_field.name, flat=True))
#                 # print(Stock.objects.values_list(
#                   # stock_field.name, flat=True).filter(tmc_id=tmc_id))
#                 obj.append(Stock.objects.values_list(
#                     stock_field.name, flat=True).get(tmc_id=tmc_id))
#         stocks[tmc_id] = obj
#     return JsonResponse(stocks)


def update_stocks_today():
    stock_list = tmc_utils.get_today_stock_list()
    clean_stock_list = tmc_utils.clean_stock_list(stock_list)
    for stock in clean_stock_list:
        _, created = Stock.objects.update_or_create(**stock)
        print("created?: " + created)
    print(len(Stock.objects.all()))


# def update_stock_history(stock):
#     get_data_url = 'http://tsetmc.ir/tsev2/data/Export-txt.aspx?t=i&a=1&b=0&i='
#     get_data_url2 = 'http://members.tsetmc.com/tsev2/data/InstTradeHistory.aspx?i='
#     get_data_url3 = '&Top=999999&A=0'
#     check = False
#     r = requests.get(get_data_url+stock.getID())
#     while r.status_code == 500:
#         if check:
#             # r = requests.get(get_data_url2+stock.getID()+get_data_url3)
#             r = requests.get(get_data_url+stock.getID())
#             check = False
#         else:
#             r = requests.get(get_data_url+stock.getID())
#             check = True
#     # print(r.text)
#     rr = r.text.split('\r\n')
#     # print(rr)
#     if len(rr) > 0:
#         del rr[-1]
#     if len(rr) > 0:
#         del rr[0]
#     # print(rr)
#     for j in rr:
#         seprated = j.split(',')
#         # print(seprated[1])
#         try:
#             found = Record.objects.get(stock=stock,date=seprated[1])
#             print('found'+str(found))
#             # for attr, value in found.__dict__.items():
#             #     print(attr, value)
#             break     # CHECKOUT THIS SHOULD BE COMMENT OR NOT!!
#         except ObjectDoesNotExist:
#             new_entry = Record.create(stock, *seprated)
#             new_entry.save()
#             print('new'+str(new_entry))
#     # print(len(Record.objects.all()))
#     # headers = ['Ticker','date','first','high','low','close','value','vol','openint','per','open','last']
#     # print([field.name for field in Record._meta.get_fields()])


# def update():
#     update_stocks_today()
#     all_stock = Stock.objects.all()
#     for i in all_stock:
#         update_stock_history(i)
#         print(list(all_stock).index(i))
