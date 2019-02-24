from django.db import models
from datetime import datetime


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
    price = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)
    profit = models.FloatField(default=0)

    def update_profit(self):
        self.profit = float(self.stock.payani) - self.price
        self.save()

    def mydelete(self):
        Bought_stock.objects.get(stock=self.stock,time=self.time,price=self.price,profit=self.profit).delete()

    def __str__(self):
        return self.stock.__str__() + ' - ' + str(self.profit)
        # return str(self.pk)


class Indicator(models.Model):
    bought = models.ManyToManyField(Bought_stock)
    name = models.CharField(max_length=300,unique = True)
    start_time = models.DateTimeField(auto_now_add=True)
    profit = models.FloatField(default=0)
    algorithm = models.CharField(max_length=500)
    last_update = models.DateTimeField(auto_now_add=True)

    def mean_of_last_days(self,days):
        # print(days)
        suggusted = []
        for stock in Stock.objects.all():
            weighted_avg = []
            # print(stock['nam'])
            # try :
            for day in days:
                to_check1 = Record.objects.filter(stock=stock).values_list('last')
                to_check1 = to_check1[:min(day,len(to_check1))]
                to_check = []
                for i in to_check1:
                    to_check.append(float(i[0]))
                div = 1
                weighted_avg.append(0)
                for i in range(0,len(to_check)):
                    # print((len(to_check)-i))
                
                    weighted_avg[days.index(day)] += (len(to_check)-i)*to_check[i]
                    div += (len(to_check)-i)
                weighted_avg[days.index(day)] /= div
                # print(weighted_avg)
                # print(stock['akharin moamele'])
            check = True
            for i in range(1,len(weighted_avg)):
                if weighted_avg[i]<=weighted_avg[i-1]:
                    check=False
            if len(days)==1:
                # print(stock['akharin moamele'])
                # print(weighted_avg[0])
                # print('')
                if weighted_avg[0]>float(stock.akharin_moamele):
                    suggusted.append(stock.getID())
            elif check:
                suggusted.append(stock.getID())
            # except:
            #     print('e')
            #     pass
        return suggusted


    def mfi(self,x,today):
        # print(x)
        suggusted = []
        for stock in Stock.objects.all():
            MFI=0
            shakhes = 0
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
                # print(today_index)
                # input()
                # print(stock)
                try:
                    temp = days[:today_index+x]
                    if not check:
                        print('halle')
                        pass
                    else:
                        print('nashod')
                except:
                    print('e')
                # input()
            print(today_index)
            # for i in range(x):
                # now = stock_records.filter()
            MFI = 1 - 1 /(1+shakhes)
            if MFI>0.5:
                suggusted.append(stock)
        return suggusted

    def update(self):
        self.update_profit()
        # self.algorithm = 'mean_of_last_days([10])'
        # self.save()
        suggusted = eval('self.'+self.algorithm)
        # print(suggusted)
        for bought in self.bought.all():
            if not bought.stock.tmc_id in suggusted:
                bought.mydelete()
        for id in suggusted:
            print(list(self.bought.all().values_list('stock', flat=True)))
            print(id)
            if int(id) not in list(self.bought.all().values_list('stock', flat=True)):
                stock = Stock.objects.get(tmc_id=id)
                bought_stock =  Bought_stock(stock=stock,price=stock.akharin_moamele)
                # print(bought_stock)
                bought_stock.save()
                self.bought.add(bought_stock)
        # print(self.bought.all())
        self.last_update = datetime.now()

    def update_profit(self):
        # self.profit = 0
        for stock in self.bought.all():
            self.profit -= stock.profit
            stock.update_profit()
            self.profit += stock.profit
            # print(self.profit)
        self.save()

    def mydelete(self):
        for bought in self.bought.all():
            bought.mydelete()
        self.delete()

    def __str__(self):
        return self.name


