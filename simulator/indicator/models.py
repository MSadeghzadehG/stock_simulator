from django.db import models
from datetime import datetime,date
from django.utils import timezone
import math
# import json
# from django.core import serializers

DEFAULT_BUY = 1000000
BUY_FEE = 0.00486
SELL_FEE = 0.01029

class Stock(models.Model):
    # id = models.BigIntegerField(unique=True, primary_key=True)
    tmc_id = models.CharField(max_length=300,unique=True)
    q1 = models.CharField(max_length=300)    
    namad = models.CharField(max_length=300)
    nam = models.CharField(max_length=300)
    q2 = models.CharField(max_length=300)
    avalin = models.CharField(max_length=300)
    payani = models.CharField(max_length=300)
    akharin_moamele = models.CharField(max_length=300)
    tedad_moamelat = models.CharField(max_length=300)
    hajm_moamelat = models.CharField(max_length=300)
    arzesh_moamelat = models.CharField(max_length=300)
    baze_rooz_kam = models.CharField(max_length=300)
    baze_rooz_ziad = models.CharField(max_length=300)
    dirooz = models.CharField(max_length=300)
    eps = models.CharField(max_length=300)
    q3 = models.CharField(max_length=300)
    q4 = models.CharField(max_length=300)
    q5 = models.CharField(max_length=300)
    q6 = models.CharField(max_length=300)    
    mojaz_ziad = models.CharField(max_length=300)
    mojaz_kam = models.CharField(max_length=300)
    q7 = models.CharField(max_length=300)
    q8 = models.CharField(max_length=300)

    def update(self,*l):
        # self.id=l[22]
        self.q1=l[0]
        self.namad = l[1]
        self.nam = l[2]
        self.q2=l[3]
        self.avalin=l[4]
        self.payani = l[5]
        self.akharin_moamele=l[6]
        self.tedad_moamelat=l[7]
        self.hajm_moamelat=l[8]
        self.arzesh_moamelat=l[9]
        self.baze_rooz_kam=l[10]
        self.baze_rooz_ziad=l[11]
        self.dirooz=l[12]
        self.eps=l[13]
        self.q3=l[14]
        self.q4=l[15]
        self.q5=l[16]
        self.q6=l[17]
        self.mojaz_ziad=l[18]
        self.mojaz_kam=l[19]
        self.q7=l[20]
        self.q8=l[21]

    def __str__(self):
        # print(self)
        return self.namad + ' ' + str(self.akharin_moamele) + ' ' + str(self.tmc_id)

    def chap(self):
        return list(self)

    def getID(self):
        return self.tmc_id


class Record(models.Model):
    stock = models.ForeignKey(Stock,on_delete=models.CASCADE)
    Ticker = models.CharField(max_length=300)
    date = models.CharField(max_length=300)
    first = models.CharField(max_length=300)
    high = models.CharField(max_length=300)
    low = models.CharField(max_length=300)
    close = models.CharField(max_length=300)
    value = models.CharField(max_length=300)
    vol = models.CharField(max_length=300)
    openint = models.CharField(max_length=300)
    per = models.CharField(max_length=300)
    openp = models.CharField(max_length=300)
    last = models.CharField(max_length=300)

    def __str__(self):
        return str(self.stock)+ ' ' + str(self.close) + ' ' + str(self.date)

    @classmethod
    def create(self,*l):
        # print(l)
        return Record(stock=l[0],
            Ticker= l[1],
            date = l[2],
            first=l[3],
            high=l[4],
            low=l[5],
            close=l[6],
            value=l[7],
            vol=l[8],
            openint=l[9],
            per=l[10],
            openp=l[11],
            last=l[12])


class Bought_stock(models.Model):
    stock = models.ForeignKey(Stock,on_delete=models.DO_NOTHING)
    time = models.DateTimeField(auto_now_add=True)
    volume = models.FloatField(default=0)
    purchase_price = models.FloatField(default=0)
    current_price = models.FloatField(default=0)
    profit = models.FloatField(default=0)


    def update_price(self,today):
        now = Record.objects.filter(stock=self.stock,date=today)
        if now.exists():
            # print('ok')
            now = now[0]
            self.current_price = float(now.close)
            self.profit = (float(self.current_price / self.purchase_price) - 1 ) * 100
            self.save()
        else:
            pass
            # print('nok')


    def mydelete(self):
        Bought_stock.objects.get(stock=self.stock,time=self.time).delete()

    def __str__(self):
        return self.stock.__str__() + ' - ' + str(self.profit)
        # return str(self.pk)


class Indicator(models.Model):
    bought = models.ManyToManyField(Bought_stock)
    name = models.CharField(max_length=300,unique = True)
    start_time = models.DateTimeField(auto_now_add=True)
    algorithm = models.CharField(max_length=300)
    paid = models.FloatField(default=0)
    bought_stocks_value = models.FloatField(default=0)
    gain = models.FloatField(default=0)
    profit = models.FloatField(default=0)
    last_update = models.DateTimeField(auto_now_add=True)


    def ema(self,x,today):
        check = True
        suggusted = []
        all_stocks = Stock.objects.all()
        for stock in all_stocks:
            weighted_avg = []
            # try :
            for day in x:
                stock_records = Record.objects.filter(stock=stock)
                to_check1 = stock_records.values_list('close')
                to_check1 = to_check1[:min(day,len(to_check1))]
                to_check = []
                for i in to_check1:
                    to_check.append(float(i[0]))
                div = 1
                weighted_avg.append(0)
                for i in range(0,len(to_check)):
                    # print((len(to_check)-i))
                    weighted_avg[x.index(day)] += (len(to_check)-i)*to_check[i]
                    div += (len(to_check)-i)
                weighted_avg[x.index(day)] /= div
                # print(weighted_avg)
            check = True
            for i in range(1,len(weighted_avg)):
                if weighted_avg[i]<=weighted_avg[i-1]:
                    check=False
            if len(x)==1:
                # print(weighted_avg[0])
                if weighted_avg[0]>float(stock_records.get(date=today).close):
                    suggusted.append(stock.getID())
            elif check:
                suggusted.append(stock.getID())
            # except:
            #     print('e')
            #     pass
        return suggusted,set(all_stocks.values_list('tmc_id',flat=True))-set(suggusted)


    def mfi(self,x,today):
        check = False
        suggusted = []
        all_stocks = Stock.objects.all()
        for stock in all_stocks:
            stock_records= Record.objects.filter(stock=stock).order_by('date')
            if stock_records.filter(date=today).exists():
                check = True
                today_index = 0
                stock_day = today
                days = list(map(int, stock_records.values_list('date',flat=True).reverse()))
                # print(today_index)
                # input()
                # print(stock)
                try:
                    temp = days[:today_index+x]
                    # print(today_index)
                    dpps = []
                    i_p = 0
                    i_n = 0
                    for i in range(x):
                        now = stock_records.get(date=str(days[today_index]))
                        # print(now.high)
                        dpp = (float(now.high) + float(now.low) + float(now.close)) / 3 * float(now.vol)
                        # print(dpp)
                        dpps.append(dpp)
                        today_index += 1
                    for i in range(x-1):
                        # print(dpps[i+1])
                        # print(dpps[i])
                        if dpps[i+1]>dpps[i]:
                            i_p += dpps[i+1]
                        else:
                            i_n += dpps[i+1]
                    # print(i_p)
                    # print(i_n)
                    # print()
                    m_indicator = i_p / i_n
                    MFI = 1 - 1 /(1+m_indicator)
                    # print(MFI)
                    if MFI>0.5:
                        # print(stock)
                        suggusted.append(stock.tmc_id)
                except:
                    # print('e')
                    pass
                    # print(days)
                    # print(today_index)
                    # input()
                # input()
        # print(suggusted)
        # print(len(suggusted))
        if check:
            return suggusted,set(all_stocks.values_list('tmc_id',flat=True))-set(suggusted)
        else:
            return [],[]


    def stockastic(self,x,today):
        check = False
        suggusted = []
        all_stocks = Stock.objects.all()
        for stock in all_stocks:
            stock_records= Record.objects.filter(stock=stock).order_by('date')
            if stock_records.filter(date=today).exists():
                check = True
                today_index = 0
                days = list(map(int, stock_records.values_list('date',flat=True).reverse()))
                try:
                    temp = days[:today_index+x]
                    # print(today_index)
                    ks = []
                    to_use_records = []
                    l = float(stock_records.get(date=str(days[today_index])).low)
                    h = float(stock_records.get(date=str(days[today_index])).high)
                    for i in range(x):
                        now = stock_records.get(date=str(days[today_index]))
                        to_use_records.append(now)
                        if float(now.high)>h:
                            h = float(now.high)
                        if float(now.low)<l:
                            l = float(now.low)
                        today_index += 1                            
                    for i in range(x):
                        now = to_use_records[i]
                        k = (float(now.close) - l) * 100 / (h-l)
                        ks.append(k)
                        today_index += 1
                    d = sum(ks[:3])/3                    
                    if ks[0]>d:
                        # print(stock)
                        suggusted.append(stock.tmc_id)
                except:
                    # print('e')
                    # print(days)
                    # print(today_index)
                    # input()
                    pass
                # input()
        # print(suggusted)
        # print(len(suggusted))        
        if check:
            return suggusted,set(all_stocks.values_list('tmc_id',flat=True))-set(suggusted)
        else:
            return [],[]


    def weekly_rule(self,x,today):
        # print(x)
        suggusted = []
        for stock in Stock.objects.all():
            to_use_records = []
            stock_records= Record.objects.filter(stock=stock).order_by('date')
            days = stock_records.values_list('date',flat=True).reverse()
            today_index = 0
            if days.exists():
                check = True
                stock_day = today
                days = list(map(int, days))
                while check and stock_day>days[-1]:
                    if stock_day in days:
                        today_index = days.index((stock_day))
                        check = False
                    else:
                        # print('bad day')
                        stock_day -= 1
                # input()
                # print(stock)
                try:
                    temp = days[today_index+7*x-1]
                    if not check:
                        # print(today_index)
                        now = stock_records.get(date=str(days[today_index]))
                        l = float(now.low)
                        h = float(now.high)
                        c = float(now.close)
                        for i in range(7*x):
                            now = stock_records.get(date=str(days[today_index]))
                            to_use_records.append(now)
                            if float(now.high)>h:
                                h = float(now.high)
                            if float(now.low)<l:
                                l = float(now.low)
                            today_index += 1                                                
                        if c>h:
                            print(stock)
                            suggusted.append(stock)
                    else:
                        print('nashod')
                except:
                    print('e')
                    # print(days)
                    # print(today_index)
                    # input()
                # input()
        print(suggusted)
        print(len(suggusted))
        return suggusted


    def rsi(self,x,today):
        check = False
        suggusted = []
        all_stocks = Stock.objects.all()
        for stock in all_stocks:
            stock_records= Record.objects.filter(stock=stock).order_by('date')
            if stock_records.filter(date=today).exists():
                check = True
                today_index = 0
                stock_day = today
                days = list(map(int, stock_records.values_list('date',flat=True).reverse()))
                # print(stock)
                try:
                    temp = days[:today_index+x]
                    prices = []
                    increasing_indexes = []
                    decreasing_indexes = []
                    for i in range(x):
                        now = stock_records.get(date=str(days[today_index]))
                        prices.append(float(now.close))
                        today_index += 1
                    for i in range(x-1):
                        # print(dpps[i+1])
                        # print(dpps[i])
                        if prices[i+1]>prices[i]:
                            increasing_indexes.append(i+1)
                        else:
                            decreasing_indexes.append(i+1)
                    # print(prices)
                    p = sum([prices[i] for i in increasing_indexes])/len(increasing_indexes)
                    n = sum([prices[i] for i in decreasing_indexes])/len(decreasing_indexes)
                    m_indicator = p/n
                    RSI = 1 - 1 /(1+m_indicator)
                    # print(RSI)
                    if RSI>0.5:
                        # print(stock)
                        suggusted.append(stock.tmc_id)
                except:
                    # print('e')
                    pass
                    # print(days)
                    # print(today_index)
                    # input()
                # input()
        # print(suggusted)
        # print(len(suggusted))
        if check:
            return suggusted,set(all_stocks.values_list('tmc_id',flat=True))-set(suggusted)
        else:
            return [],[]

    
    def ma(self,days,today):
        pass

    
    def aoc(self,x,today):
        check = False
        suggusted = []
        all_stocks = Stock.objects.all()
        for stock in all_stocks:
            stock_records= Record.objects.filter(stock=stock).order_by('date')
            if stock_records.filter(date=today).exists():
                check = True
                today_index = 0
                stock_day = today
                days = list(map(int, stock_records.values_list('date',flat=True).reverse()))
                # print(today_index)
                # input()
                # print(stock)
                try:
                    # print(today_index)
                    now = float(stock_records.filter(date=str(days[today_index]))[0].close)
                    last = float(stock_records.filter(date=str(days[today_index+x-1]))[0].close)
                    if now>last:
                        # print(stock)
                        suggusted.append(stock.tmc_id)
                except:
                    # print('e')
                    pass
                    # print(days)
                    # print(today_index)
                    # input()
                # input()
        # print(suggusted)
        # print(len(suggusted))
        if check:
            return suggusted,set(all_stocks.values_list('tmc_id',flat=True))-set(suggusted)
        else:
            return [],[]


    def update_control(self,start_day,end_day):
        log = []
        today = start_day
        while today<end_day:
            self.update(today)
            print(today)
            if today%10000==1231:
                today = (int(today/10000) + 1)*10000 + 100
            if today%100 == 31:
                today += 69
            today += 1
            o = {}
            for i in Indicator._meta.get_fields():
                o['date'] = today
                o[i.name] = getattr(self,i.name)
            # for i in list(o['bought'].all()):
            log.append(o)
            # print(log)


    def update_today(self):
        today = int(''.join(map(str, str(date.today()).split('-'))))
        print(today)
        for stock in self.bought.all():
            if not Record.objects.filter(stock=stock,date=today).exists():
                today_record = Record(stock=stock,date=today,first=stock.avalin,high=stock.baze_rooz_ziad,low=stock.baze_rooz_kam,close=stock.akharin_moamele,\
                    value=stock.arzesh_moamelat,vol=stock.hajm_moamelat,openint=0,per='d',openp=0,last=stock.payani)
                
                pass


    def update(self,today):
        self.update_profit(today)
        # self.algorithm = 'mean_of_last_days([10])'
        # self.save()
        to_buy,to_sell = eval('self.'+self.algorithm.split(')')[0]+','+str(today)+')')
        print(len(to_buy))
        print(len(to_sell))
        boughts = self.bought.all()
        # print(suggusted)
        # print(boughts)
        for bought in boughts:
            if bought.stock.tmc_id in to_sell:                
                self.gain += bought.current_price * bought.volume
                bought.mydelete()
                print('deleted')
        for id in to_buy:
            if int(id) not in list(boughts.values_list('stock', flat=True)):
                stock = Stock.objects.get(tmc_id=id)
                price = Record.objects.filter(stock=stock,date=today)
                # print(stock.akharin_moamele)
                if price.exists():
                    price = float(price[0].close)
                    volume = math.ceil(DEFAULT_BUY/price)
                    # print(volume,price)
                    bought_stock = Bought_stock(stock=stock,purchase_price=price,current_price=price,volume=volume)
                    self.paid += price * volume
                    print('bought_stock')
                    bought_stock.save()
                    self.bought.add(bought_stock)
        # print(self.bought.all())
        # print(self.last_update)
        # print(datetime.now())
        self.last_update = datetime.now(tz=timezone.utc)
        self.save()
        # print(self.last_update)


    def update_profit(self,today):
        self.bought_stocks_value = 0
        for stock in self.bought.all():
            # self.profit -= stock.profit * stock.volume
            stock.update_price(today)
            self.bought_stocks_value += stock.current_price * stock.volume
            # print(self.profit)
        if self.paid>0:
            self.profit = (float((self.gain + self.bought_stocks_value) / self.paid) - 1) * 100
        self.save()


    def mydelete(self):
        for bought in self.bought.all():
            bought.mydelete()
        self.delete()


    def __str__(self):
        return self.name


