from django.shortcuts import render,redirect
from django.http import HttpResponse
from indicator.models import Stock,Record,Indicator,Bought_stock
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.template import loader
from datetime import datetime
import os,csv
from django import forms
import requests


class IndicatorForm(forms.Form):
    name = forms.CharField(max_length=100)
    algorithm = forms.CharField(max_length=200)

def home(request):
    form = IndicatorForm(auto_id=False)
    template = loader.get_template('indicator/home.html')
    context = { 'form' : form }
    return HttpResponse(template.render(context, request))


def stocks_table(request):
    template = loader.get_template('indicator/stocks.html')
    context = { 'stocks': serializers.serialize("python",Stock.objects.all()) , 'headers':[field.name for field in Stock._meta.get_fields()][3:]}
    return HttpResponse(template.render(context, request))


def records_table(request,id):
    template = loader.get_template('indicator/records.html')
    stock = Stock.objects.get(tmc_id=id)
    records = Record.objects.filter(stock=stock)
    context = { 'records': serializers.serialize("python",records) , 'headers':[field.name for field in Record._meta.get_fields()][1:]}
    return HttpResponse(template.render(context, request))


def boughts_table(request,name):
    template = loader.get_template('indicator/bought.html')
    indicator = Indicator.objects.get(name=name)
    indicator.update_profit()
    boughts = indicator.bought.all()
    context = { 'stocks': serializers.serialize("python",boughts) , 'headers':[field.name for field in Bought_stock._meta.get_fields()][2:]}
    return HttpResponse(template.render(context, request))


def indicators_table(request):
    print(len(Indicator.objects.all()))
    indicators = Indicator.objects.all()
    for indicator in indicators:
        indicator.update()


    template = loader.get_template('indicator/indicators.html')
    context = { 'indicators': serializers.serialize("python",indicators) , 'headers':[field.name for field in Indicator._meta.get_fields()][1:-1]}
    return HttpResponse(template.render(context, request))


def add_indicator(request):
     # if this is a POST request we need to process the form data
      # create a form instance and populate it with data from the request:
    form = IndicatorForm(request.POST)
    # check whether it's valid:
    if form.is_valid():
        new_indicator = Indicator(name=form.cleaned_data['name'],algorithm=form.cleaned_data['algorithm'])
        new_indicator.save()
    return redirect('')

    


def delete_indicator(request,name):
    indicator = Indicator.objects.all().get(name=name)
    # print(indicator)
    indicator.mydelete()
    print(len(Indicator.objects.all()))
    print(len(Bought_stock.objects.all()))
    return redirect('indicators')

def update_indicator(request,name):
    indicator = Indicator.objects.all().get(name=name)
    print(indicator)
    indicator.update()
    return redirect('indicators')


def delete_database(request):
    # Record.objects.all().delete()
    # Stock.objects.all().delete()
    # Indicator.objects.all().delete()
    for o in Indicator.objects.all():
        o.mydelete()
    print(len(Indicator.objects.all()))
    # Bought_stock.objects.all().delete()
    print(len(Bought_stock.objects.all()))
    return HttpResponse('deleted')


def update(request):
    get_data_url = 'http://tsetmc.ir/tsev2/data/Export-txt.aspx?t=i&a=1&b=0&i='
    r = requests.get('http://www.tsetmc.com/tsev2/data/MarketWatchInit.aspx?h=0&r=0')
   
    # headers = ['id','?','namad','nam','?','avalin','payani','akharin moamele','tedad moamelat','hajm moamelat','arzesh mamelat','baze rooz kam','baze rooz ziad','dirooz','eps','?','?','?','?','mojaz ziad','mojaz kam','?','?']
    # print(len(r.text.split('@')[2].split(';')))
    # print(len(Stock.objects.all()))
    stocks_list = r.text.split('@')[2].split(';')
    # print(stocks_list)
    for i in stocks_list:
        # print(i.split(',')[:23])
        seprated = i.split(',')[:23]
        print(seprated)
        new_entry = Stock(*seprated)
        # sleep(1)
        try:
            found = Stock.objects.get(tmc_id = seprated[0])
            found.update(*seprated[1:])
            print('found'+str(found))
            found.save()
        except ObjectDoesNotExist:
            print('new'+str(new_entry))
            new_entry.save()       
    print(len(Stock.objects.all()))
    # print([field.name for field in Stock._meta.get_fields()])

    # pdf_headers = ['Ticker','date','first','high','low','close','value','vol','openint','per','open','last']
    print([field.name for field in Record._meta.get_fields()])
    print(len(Record.objects.all()))
    all_stock = Stock.objects.all()
    for i in all_stock:
        # print(i)
        r = requests.get(get_data_url+i.getID())
        # print(request.text)
        rr = r.text.split('\r\n')
        # print(rr)
        if len(rr)>0:
            del rr[-1]
        if len(rr)>0:
            del rr[0]
        # print(rr)
        for j in rr:
            seprated = j.split(',')
            # print(seprated[1])
            try:
                found = Record.objects.get(stock = i, date = seprated[1])
                print('found'+str(found))
                # for attr, value in found.__dict__.items():
                #     print(attr, value)
                # input()
                break
                # print('here')
            except ObjectDoesNotExist:
                new_entry = Record.create(i,*seprated)
                new_entry.save()
                print('new'+str(new_entry))

        # print(len(Record.objects.all()))
        print(list(all_stock).index(i),i)
    return redirect('/stocks')