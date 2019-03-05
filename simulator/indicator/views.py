from django.shortcuts import render,redirect
from django.http import HttpResponse
from indicator.models import Stock,Record,Indicator,Bought_stock
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.template import loader
from datetime import datetime,date
import os,datetime
from django import forms
import requests
from background_task import background


class IndicatorForm(forms.Form):
    name = forms.CharField(max_length=100)
    algorithm = forms.CharField(max_length=200)
    days = forms.CheckboxInput()


class EmailForm(forms.Form):
    firstname = forms.CharField(max_length=255)
    lastname = forms.CharField(max_length=255)
    email = forms.EmailField()
    subject = forms.CharField(max_length=255)
    botcheck = forms.CharField(max_length=5)
    message = forms.CharField()


# from django.core.mail import send_mail, BadHeaderError
# def sendmail(request):
#     if request.method == 'POST':
#         form = EmailForm(request.POST)
#         if form.is_valid():
#             firstname = form.cleaned_data['firstname']
#             lastname = form.cleaned_data['lastname']
#             email = form.cleaned_data['email']
#             subject = form.cleaned_data['subject']
#             botcheck = form.cleaned_data['botcheck'].lower()
#             message = form.cleaned_data['message']
#             if botcheck == 'yes':
#                 try:
#                     fullemail = firstname + " " + lastname + " " + "<" + email + ">"
#                     send_mail(subject, message, fullemail, ['SENDTOUSER@DOMAIN.COM'])
#                     return HttpResponseRedirect('/email/thankyou/')
#                 except:
#                     return HttpResponseRedirect('/email/')
#         else:
#             return HttpResponseRedirect('/email/')
#     else:
#         return HttpResponseRedirect('/email/')  


@background(schedule=60)
def update_indicators():
    indicators = Indicator.objects.all()
    # print('here')
    today = int(''.join(map(str, str(date.today()).split('-'))))
    print(today)
    for indicator in indicators:
        indicator.update(today=20190210)
    print('updated')
    print(datetime.datetime.now())


def home(request):
    form = IndicatorForm(auto_id=False)
    # print(Bought_stock.objects.all())
    template = loader.get_template('indicator/home.html')
    context = { 'form' : form }
    return HttpResponse(template.render(context, request))


def stocks_table(request):
    from django.db.models import IntegerField
    from django.db.models.functions import Cast
    template = loader.get_template('indicator/stocks.html')
    stocks = Stock.objects.annotate(my_integer_field=Cast('hajm_moamelat', IntegerField())).order_by('my_integer_field', 'hajm_moamelat').reverse()
    context = { 'stocks': serializers.serialize("python",stocks) , 'headers':[field.name for field in Stock._meta.get_fields()][3:]}
    return HttpResponse(template.render(context, request))


def records_table(request,id):
    template = loader.get_template('indicator/records.html')
    stock = Stock.objects.get(tmc_id=id)
    records = Record.objects.filter(stock=stock).order_by('date').reverse()
    context = { 'records': serializers.serialize("python",records) , 'headers':[field.name for field in Record._meta.get_fields()][1:]}
    return HttpResponse(template.render(context, request))


def boughts_table(request,name):
    template = loader.get_template('indicator/bought.html')
    indicator = Indicator.objects.get(name=name)
    # indicator.update_profit()
    boughts = indicator.bought.all().order_by('profit').reverse()
    context = { 'stocks': serializers.serialize("python",boughts) , 'headers':[field.name for field in Bought_stock._meta.get_fields()][2:]}
    return HttpResponse(template.render(context, request))


def indicators_table(request):
    # print(len(Indicator.objects.all()))
    indicators = Indicator.objects.defer('bought')
    # print(indicators[0].bought)
    # update_indicators(schedule=60)#,repeat_until=None)
    # update_indicators(serializers.serialize("python",indicators),repeat=1,repeat_until=None)
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
    return redirect('/indicators')


def delete_indicator(request,name):
    indicator = Indicator.objects.all().get(name=name)
    # print(indicator)
    indicator.mydelete()
    print(len(Indicator.objects.all()))
    print(len(Bought_stock.objects.all()))
    return redirect('/indicators')


def update_indicator(request,name):
    indicator = Indicator.objects.all().get(name=name)
    print(indicator)
    today = int(''.join(map(str, str(date.today()).split('-'))))
    print(today)
    indicator.update_control(20181130,20181230)
    return redirect('/indicators')


def delete_database(request):
    # Record.objects.all().delete()
    # Stock.objects.all().delete()
    # Indicator.objects.all().delete()
    # for o in Indicator.objects.all():
    #     o.mydelete()
    # print(len(Indicator.objects.all()))
    Bought_stock.objects.all().delete()
    print(len(Bought_stock.objects.all()))
    return HttpResponse('deleted')


def update(request):
    get_data_url = 'http://tsetmc.ir/tsev2/data/Export-txt.aspx?t=i&a=1&b=0&i='
    get_data_url2 = 'http://members.tsetmc.com/tsev2/data/InstTradeHistory.aspx?i='
    get_data_url3 = '&Top=999999&A=0'
    r = requests.get('http://www.tsetmc.com/tsev2/data/MarketWatchInit.aspx?h=0&r=0')
    # headers = ['id','?','namad','nam','?','avalin','payani','akharin moamele','tedad moamelat','hajm moamelat','arzesh mamelat','baze rooz kam','baze rooz ziad','dirooz','eps','?','?','?','?','mojaz ziad','mojaz kam','?','?']
    # print(len(r.text.split('@')[2].split(';')))
    print(len(Record.objects.all()))
    print(len(Stock.objects.all()))
    stocks_list = r.text.split('@')[2].split(';')
    # print(stocks_list)
    for i in stocks_list:
        # print(i.split(',')[:23])
        seprated = i.split(',')[:23]
        # print(seprated)
        # sleep(1)
        new_entry = Stock(seprated[0],*seprated)
        try:
            found = Stock.objects.get(tmc_id = seprated[0])
            found.update(*seprated[1:])
            # found.save(id=seprated[0])
            print('found'+str(found))
            found.save()
        except ObjectDoesNotExist:
            print('new'+str(new_entry))
            new_entry.save()       
    print(len(Stock.objects.all()))
    # print([field.name for field in Stock._meta.get_fields()])
    # pdf_headers = ['Ticker','date','first','high','low','close','value','vol','openint','per','open','last']
    # print([field.name for field in Record._meta.get_fields()])
    all_stock = Stock.objects.all()
    for i in all_stock:
        # print(i)
        check = False
        r = requests.get(get_data_url+i.getID())
        while r.status_code==500:
            if check:
                # r = requests.get(get_data_url2+i.getID()+get_data_url3)
                r = requests.get(get_data_url+i.getID())
                check = False
            else:
                r = requests.get(get_data_url+i.getID())
                check = True
        # print(r.text)
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
        print(list(all_stock).index(i))
    return redirect('/stocks')