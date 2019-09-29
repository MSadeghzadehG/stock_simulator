import requests
from indicator.models import Stock


def get_today_stock_list():
    get_today_stock_url = (
        "http://www.tsetmc.com/tsev2/data/MarketWatchInit.aspx?h=0&r=0"
    )
    r = requests.get(get_today_stock_url)
    # headers = ['id','?','namad','nam','?','avalin','payani','akharin moamele','tedad moamelat','hajm moamelat','arzesh mamelat','baze rooz kam','baze rooz ziad','dirooz','eps','?','?','?','?','mojaz ziad','mojaz kam','?','?']
    stock_list = r.text.split("@")[2].split(";")
    return stock_list


def clean_stock_list(stock_list):
    remove_list = [1, 3, 4, 13, 15, 16, 17, 18, 21, 22]
    clean_stock_list = []
    stock_fields = [field.name for field in Stock._meta.get_fields()][1:]
    for str_stock in stock_list:
        stock = str_stock.split(",")[:23]
        for i in range(23):
            if i in remove_list:
                stock.pop(i - remove_list.index(i))
        dict_stock = {}
        for i in range(len(stock_fields)):
            dict_stock[stock_fields[i]] = stock[i]
        clean_stock_list.append(dict_stock)
    return clean_stock_list
