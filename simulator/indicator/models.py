from django.db import models
from datetime import datetime, date
from django.utils import timezone
import math


DEFAULT_BUY = 1000000
BUY_FEE = 0.00486
SELL_FEE = 0.01029
check_stock_id = 53449700212786324


# ['id','?','namad','?','?','avalin','payani','akharin moamele','tedad moamelat','hajm moamelat','arzesh mamelat','baze rooz kam','baze rooz ziad','dirooz','eps','?','?','?','?','mojaz ziad','mojaz kam','?','?']
class Stock(models.Model):
    tmc_id = models.BigIntegerField(primary_key=True)
    namad = models.CharField(max_length=300)
    avalin = models.FloatField()
    payani = models.FloatField()
    akharin_moamele = models.FloatField()
    tedad_moamelat = models.FloatField()
    hajm_moamelat = models.FloatField()
    arzesh_moamelat = models.FloatField()
    baze_rooz_kam = models.FloatField()
    baze_rooz_ziad = models.FloatField()
    eps = models.FloatField()
    mojaz_ziad = models.FloatField()
    mojaz_kam = models.FloatField()

    def __str__(self):
        return self.namad + " " + str(self.tmc_id)


class StockLog(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()
    first = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    value = models.FloatField()
    volume = models.FloatField()
    last = models.FloatField()

    def __str__(self):
        return str(self.stock) + " " + str(self.date)


class Indicator(models.Model):
    name = models.CharField(max_length=300, unique=True)
    start_time = models.DateField(auto_now_add=False)
    end_time = models.DateField(auto_now_add=False, null=True, default=None)
    algorithm = models.CharField(max_length=300)
    paid = models.FloatField(default=0)
    bought_stocks_value = models.FloatField(default=0)
    gain = models.FloatField(default=0)
    profit = models.FloatField(default=0)
    # last_update = models.DateField(auto_now_add=False, null=True, default=None)

    def datetime_to_dateint(time):
        return int("".join(map(str, str(time.date()).split("-"))))

    def add_time_to_date(date):
        return datetime.combine(date, datetime.now().time())

    def dateint_to_datetime(date):
        date = str(date)
        date = date[0:4] + "-" + date[4:6] + "-" + date[6:]
        return datetime.strptime(date, "%Y-%m-%d").date()


#     def algo_ema(self, x, today):
#         to_buy = []
#         to_sell = []
#         all_stocks = Stock.objects.all()
#         is_valid = False
#         for stock in all_stocks:
#             if stock.tmc_id == check_stock_id:
#                 print("YEEESSSS")
#             weighted_avg = []
#             stock_records = (
#                 Record.objects.filter(stock=stock).order_by("date").reverse()
#             )
#             # print(stock_records)
#             last_prices = list(stock_records.values_list("last", flat=True))
#             if stock_records.filter(date=str(today)).exists():
#                 today_index = list(stock_records.values_list("date", flat=True)).index(
#                     str(today)
#                 )
#                 enough_days = True
#                 for day in x:
#                     day_range_prices = last_prices[today_index : today_index + day]
#                     to_check = []
#                     if stock.tmc_id == check_stock_id:
#                         print(day_range_prices)
#                     for i in day_range_prices:
#                         to_check.append(float(i))
#                     div = 0
#                     weighted_avg.append(0)
#                     if len(to_check) < day:
#                         enough_days = False
#                         break
#                     for i in range(len(to_check)):
#                         weighted_avg[x.index(day)] += (len(to_check) - i) * to_check[i]
#                         div += len(to_check) - i
#                     if stock.tmc_id == check_stock_id:
#                         print(weighted_avg[x.index(day)], div)
#                     weighted_avg[x.index(day)] /= div
#                 increase_check = True
#                 decrease_check = True
#                 if stock.tmc_id == check_stock_id:
#                     print(weighted_avg)
#                 for i in range(1, len(weighted_avg)):
#                     if weighted_avg[i] <= weighted_avg[i - 1]:
#                         increase_check = False
#                     if weighted_avg[i] >= weighted_avg[i - 1]:
#                         decrease_check = False
#                 if len(x) == 1:
#                     # print(weighted_avg[0])
#                     if (
#                         weighted_avg[0] > float(stock_records.get(date=today).last)
#                         and enough_days
#                     ):
#                         to_buy.append(stock.getID())
#                         is_valid = True
#                 elif enough_days:
#                     if stock.tmc_id == check_stock_id:
#                         print(increase_check, decrease_check)
#                     if decrease_check:
#                         to_buy.append(stock.getID())
#                         is_valid = True
#                     if increase_check:
#                         to_sell.append(stock.getID())
#                         is_valid = True
#         print(str(check_stock_id) in to_buy)
#         print(str(check_stock_id) in to_sell)
#         if is_valid:
#             return to_buy, to_sell
#         else:
#             return [], []

#     def algo_mfi(self, x, today):
#         x = x[0]
#         check = False
#         suggusted = []
#         all_stocks = Stock.objects.all()
#         for stock in all_stocks:
#             stock_records = Record.objects.filter(stock=stock).order_by("date")
#             if stock_records.filter(date=today).exists():
#                 check = True
#                 today_index = 0
#                 stock_day = today
#                 days = list(
#                     map(int, stock_records.values_list("date", flat=True).reverse())
#                 )
#                 # print(today_index)
#                 # input()
#                 # print(stock)
#                 try:
#                     temp = days[: today_index + x]
#                     # print(today_index)
#                     dpps = []
#                     i_p = 0
#                     i_n = 0
#                     for i in range(x):
#                         now = stock_records.get(date=str(days[today_index]))
#                         # print(now.high)
#                         dpp = (
#                             (float(now.high) + float(now.low) + float(now.last))
#                             / 3
#                             * float(now.vol)
#                         )
#                         # print(dpp)
#                         dpps.append(dpp)
#                         today_index += 1
#                     for i in range(x - 1):
#                         # print(dpps[i+1])
#                         # print(dpps[i])
#                         if dpps[i + 1] > dpps[i]:
#                             i_p += dpps[i + 1]
#                         else:
#                             i_n += dpps[i + 1]
#                     # print(i_p)
#                     # print(i_n)
#                     # print()
#                     m_indicator = i_p / i_n
#                     MFI = 1 - 1 / (1 + m_indicator)
#                     # print(MFI)
#                     if MFI > 0.5:
#                         # print(stock)
#                         suggusted.append(stock.tmc_id)
#                 except:
#                     # print('e')
#                     pass
#                     # print(days)
#                     # print(today_index)
#                     # input()
#                 # input()
#         # print(suggusted)
#         # print(len(suggusted))
#         if check:
#             return (
#                 suggusted,
#                 set(all_stocks.values_list("tmc_id", flat=True)) - set(suggusted),
#             )
#         else:
#             return [], []

#     def algo_stockastic(self, x, today):
#         x = x[0]
#         check = False
#         suggusted = []
#         all_stocks = Stock.objects.all()
#         for stock in all_stocks:
#             stock_records = Record.objects.filter(stock=stock).order_by("date")
#             if stock_records.filter(date=today).exists():
#                 check = True
#                 today_index = 0
#                 days = list(
#                     map(int, stock_records.values_list("date", flat=True).reverse())
#                 )
#                 try:
#                     temp = days[: today_index + x]
#                     # print(today_index)
#                     ks = []
#                     to_use_records = []
#                     l = float(stock_records.get(date=str(days[today_index])).low)
#                     h = float(stock_records.get(date=str(days[today_index])).high)
#                     for i in range(x):
#                         now = stock_records.get(date=str(days[today_index]))
#                         to_use_records.append(now)
#                         if float(now.high) > h:
#                             h = float(now.high)
#                         if float(now.low) < l:
#                             l = float(now.low)
#                         today_index += 1
#                     for i in range(x):
#                         now = to_use_records[i]
#                         k = (float(now.last) - l) * 100 / (h - l)
#                         ks.append(k)
#                         today_index += 1
#                     d = sum(ks[:3]) / 3
#                     if ks[0] > d:
#                         # print(stock)
#                         suggusted.append(stock.tmc_id)
#                 except:
#                     # print('e')
#                     # print(days)
#                     # print(today_index)
#                     # input()
#                     pass
#                 # input()
#         # print(suggusted)
#         # print(len(suggusted))
#         if check:
#             return suggusted, set(all_stocks.values_list("tmc_id", flat=True))
#             -set(suggusted)
#         else:
#             return [], []

#     def algo_weekly(self, x, today):
#         x = x[0]
#         to_buy = []
#         to_sell = []
#         all_stocks = Stock.objects.all()
#         check = False
#         for stock in all_stocks:
#             to_use_records = []
#             stock_records = Record.objects.filter(stock=stock).order_by("date")
#             if stock_records.filter(date=today).exists():
#                 check = True
#                 today_index = 0
#                 days = list(
#                     map(int, stock_records.values_list("date", flat=True).reverse())
#                 )
#                 # print(stock)
#                 try:
#                     temp = days[today_index + 7 * x - 1]
#                     now = stock_records.get(date=str(days[today_index]))
#                     l = float(now.last)
#                     h = 0
#                     c = float(now.last)
#                     today_index = 1
#                     for i in range(1, 7 * x):
#                         now = stock_records.get(date=str(days[today_index]))
#                         to_use_records.append(now)
#                         if float(now.high) > h:
#                             h = float(now.high)
#                         if float(now.low) < l:
#                             l = float(now.low)
#                         today_index += 1
#                     # print(c,l,h)
#                     if c > h:
#                         # print(stock)
#                         to_buy.append(stock.tmc_id)
#                     elif c < l:
#                         to_sell.append(stock.tmc_id)
#                 except:
#                     # print('e')
#                     # print(days)
#                     # print(today_index)
#                     # input()
#                     pass
#                 # input()
#         if check:
#             return to_buy, to_sell
#         else:
#             return [], []

#     def algo_rsi(self, x, today):
#         x = x[0]
#         check = False
#         suggusted = []
#         all_stocks = Stock.objects.all()
#         for stock in all_stocks:
#             stock_records = Record.objects.filter(stock=stock).order_by("date")
#             if stock_records.filter(date=today).exists():
#                 check = True
#                 today_index = 0
#                 stock_day = today
#                 days = list(
#                     map(int, stock_records.values_list("date", flat=True).reverse())
#                 )
#                 # print(stock)
#                 try:
#                     temp = days[: today_index + x]
#                     prices = []
#                     increasing_indexes = []
#                     decreasing_indexes = []
#                     for i in range(x):
#                         now = stock_records.get(date=str(days[today_index]))
#                         prices.append(float(now.last))
#                         today_index += 1
#                     for i in range(x - 1):
#                         # print(dpps[i+1])
#                         # print(dpps[i])
#                         if prices[i + 1] > prices[i]:
#                             increasing_indexes.append(i + 1)
#                         else:
#                             decreasing_indexes.append(i + 1)
#                     # print(prices)
#                     p = sum([prices[i] for i in increasing_indexes]) / len(
#                         increasing_indexes
#                     )
#                     n = sum([prices[i] for i in decreasing_indexes]) / len(
#                         decreasing_indexes
#                     )
#                     m_indicator = p / n
#                     RSI = 1 - 1 / (1 + m_indicator)
#                     # print(RSI)
#                     if RSI > 0.5:
#                         # print(stock)
#                         suggusted.append(stock.tmc_id)
#                 except:
#                     # print('e')
#                     pass
#                     # print(days)
#                     # print(today_index)
#                     # input()
#                 # input()
#         # print(suggusted)
#         # print(len(suggusted))
#         if check:
#             return suggusted, set(all_stocks.values_list("tmc_id", flat=True))
#             -set(suggusted)
#         else:
#             return [], []

#     def algo_ma(self, x, today):
#         to_buy = []
#         to_sell = []
#         all_stocks = Stock.objects.all()
#         is_valid = False
#         for stock in all_stocks:
#             weighted_avg = []
#             stock_records = Record.objects.filter(stock=stock).order_by("date")
#             last_prices = list(stock_records.values_list("last", flat=True))
#             if stock_records.filter(date=str(today)).exists():
#                 today_index = list(stock_records.values_list("date", flat=True)).index(
#                     str(today)
#                 )
#                 for day in x:
#                     day_range_prices = last_prices[today_index : today_index + day]
#                     to_check = []
#                     for i in day_range_prices:
#                         to_check.append(float(i))
#                     weighted_avg.append(sum(to_check) / len(to_check))
#                 increase_check = True
#                 decrease_check = True
#                 # print(weighted_avg)
#                 for i in range(1, len(weighted_avg)):
#                     if weighted_avg[i] <= weighted_avg[i - 1]:
#                         increase_check = False
#                     if weighted_avg[i] >= weighted_avg[i - 1]:
#                         decrease_check = False
#                 if len(x) == 1:
#                     # print(weighted_avg[0])
#                     if weighted_avg[0] > float(stock_records.get(date=today).last):
#                         to_buy.append(stock.getID())
#                         is_valid = True
#                 else:
#                     if increase_check:
#                         to_buy.append(stock.getID())
#                         is_valid = True
#                     if decrease_check:
#                         to_sell.append(stock.getID())
#                         is_valid = True
#         if is_valid:
#             return to_buy, to_sell
#         else:
#             return [], []

#     def algo_aoc(self, x, today):
#         x = x[0]
#         check = False
#         suggusted = []
#         all_stocks = Stock.objects.all()
#         for stock in all_stocks:
#             stock_records = Record.objects.filter(stock=stock).order_by("date")
#             if stock_records.filter(date=today).exists():
#                 check = True
#                 today_index = 0
#                 stock_day = today
#                 days = list(
#                     map(int, stock_records.values_list("date", flat=True).reverse())
#                 )
#                 # print(today_index)
#                 # input()
#                 # print(stock)
#                 try:
#                     # print(today_index)
#                     now = float(
#                         stock_records.filter(date=str(days[today_index]))[0].last
#                     )
#                     last = float(
#                         stock_records.filter(date=str(days[today_index + x - 1]))[
#                             0
#                         ].last
#                     )
#                     if now > last:
#                         # print(stock)
#                         suggusted.append(stock.tmc_id)
#                 except:
#                     # print('e')
#                     pass
#                     # print(days)
#                     # print(today_index)
#                     # input()
#                 # input()
#         # print(suggusted)
#         # print(len(suggusted))
#         if check:
#             return suggusted, set(all_stocks.values_list("tmc_id", flat=True))
#             -set(suggusted)
#         else:
#             return [], []

#     def update_time_control(self):
#         end_time = self.end_time
#         if end_time is None:
#             end_time = datetime.now()
#         start_time = self.last_update
#         if self.last_update is None:
#             start_time = self.start_time
#         if Indicator.datetime_to_dateint(start_time) != Indicator.datetime_to_dateint(
#             end_time
#         ):
#             self.update_procedure_control(
#                 Indicator.datetime_to_dateint(start_time),
#                 Indicator.datetime_to_dateint(end_time),
#             )

#     def update_procedure_control(self, start_day, end_day):
#         today = start_day
#         while today < end_day:
#             self.update(today)
#             print(self.name, ":", today)
#             if today % 10000 == 1231:
#                 today = (int(today / 10000) + 1) * 10000 + 100
#             if today % 100 == 31:
#                 today += 69
#             today += 1

#     def update(self, today):
#         try:
#             self.last_update = Indicator.add_time_to_date(
#                 Indicator.dateint_to_datetime(today)
#             )
#         except:
#             return
#         self.update_profit(today)
#         # self.algorithm = 'algo_ma([10])'
#         # self.save()
#         to_buy, to_sell = eval(
#             "self.algo_" + self.algorithm.split(")")[0] + "," + str(today) + ")"
#         )
#         print(len(to_buy))
#         print(len(to_sell))
#         print(to_sell)
#         boughts = self.bought.all()
#         # print(suggusted)
#         # print(boughts)
#         for bought in boughts:
#             # print(bought.stock.tmc_id)
#             if bought.stock.getID() in to_sell:
#                 self.gain += bought.current_price * bought.volume
#                 # bought.mydelete()
#                 # print(len(self.bought.all()))
#                 # print(len(self.trade_log.all()))
#                 self.bought.remove(bought)
#                 # print(len(self.bought.all()))
#                 # print(len(self.trade_log.all()))
#                 bought.sell_time = Indicator.add_time_to_date(
#                     Indicator.dateint_to_datetime(today)
#                 )
#                 bought.save()
#                 print(self.name, ": deleted")
#                 # input()
#         for id in to_buy:
#             stock = Stock.objects.get(tmc_id=id)
#             if stock.tmc_id not in list(boughts.values_list("stock_id", flat=True)):
#                 price = Record.objects.filter(stock=stock, date=today)
#                 # print(stock.akharin_moamele)
#                 if price.exists():
#                     price = float(price[0].last)
#                     volume = math.ceil(DEFAULT_BUY / price)
#                     # print(volume,price)
#                     bought_stock = Bought_stock(
#                         stock=stock,
#                         purchase_price=price,
#                         current_price=price,
#                         volume=volume,
#                     )
#                     bought_stock.buy_time = Indicator.add_time_to_date(
#                         Indicator.dateint_to_datetime(today)
#                     )
#                     self.paid += price * volume
#                     print(self.name, ": bought_stock")
#                     bought_stock.save()
#                     self.bought.add(bought_stock)
#                     self.trade_log.add(bought_stock)
#         # print(self.bought.all())
#         # print(self.last_update)
#         # print(datetime.now())
#         self.save()
#         # print(self.last_update)

#     def update_profit(self, today):
#         self.bought_stocks_value = 0
#         for stock in self.bought.all():
#             # self.profit -= stock.profit * stock.volume
#             stock.update_price(today)
#             self.bought_stocks_value += stock.current_price * stock.volume
#             # print(self.profit)
#         if self.paid > 0:
#             self.profit = (
#                 float((self.gain + self.bought_stocks_value) / self.paid) - 1
#             ) * 100
#         self.save()

#     def mydelete(self):
#         for bought in self.bought.all():
#             bought.mydelete()
#         for bought in self.trade_log.all():
#             bought.mydelete()
#         self.delete()

#     def __str__(self):
#         return self.name


class TradeLog(models.Model):
    indicator = models.ForeignKey(Indicator, on_delete=models.DO_NOTHING, null=False)
    buy_stock_log = models.ForeignKey(
        StockLog, on_delete=models.DO_NOTHING, null=False, related_name="buy"
    )
    sell_stock_log = models.ForeignKey(
        StockLog,
        on_delete=models.DO_NOTHING,
        null=True,
        default=None,
        related_name="sell",
    )
    volume = models.FloatField(default=0)
    profit = models.FloatField(default=None, null=True)

    def __str__(self):
        return (
            self.indicator.__str__()
            + " - "
            + self.buy_stock_log.__str__()
            + " - "
            + str(self.profit)
        )
