import requests
from indicator.models import Stock
import logging
logger = logging.getLogger('django')


def get_today_stock_list():
    get_today_stock_url = (
        "http://www.tsetmc.com/tsev2/data/MarketWatchInit.aspx?h=0&r=0"
    )
    row_data = requests.get(get_today_stock_url)
    stock_list = row_data.text.split("@")[2].split(";")
    logger.info('today stock list fetched')
    return stock_list


def correct_stock_types(stock, stock_fields):
    correct_stock = []
    correct_stock.append(int(stock[0]))
    correct_stock.append(str(stock[1]))
    return correct_stock


def remove_redundent_elements(input_list, remove_list):
    starting_length = len(input_list)
    for i in range(starting_length):
        if i in remove_list:
            input_list.pop(i - remove_list.index(i))
    return input_list


def clean_stock_list(stock_list):
    remove_list = [1, 3, 4, 13, 15, 16, 17, 18, 21, 22]
    clean_stock_list = []
    stock_fields = [field for field in Stock._meta.get_fields()][1:]
    # print(dir(stock_fields[0]))
    for str_stock in stock_list:
        stock = str_stock.split(",")[:23]
        stock = remove_redundent_elements(stock, remove_list)
        stock = correct_stock_types(stock, stock_fields)
        dict_stock = {}
        for i in range(len(stock_fields)):
            dict_stock[stock_fields[i].name] = stock[i]
        clean_stock_list.append(dict_stock)
    return clean_stock_list


def clean_stock_logs(stock_logs):
    if len(stock_logs) > 0:
        del stock_logs[0]
    logger.info(stock_logs[1])
    return stock_logs


def get_stock_logs(stock):
    get_data_url = 'http://tsetmc.ir/tsev2/data/Export-txt.aspx?t=i&a=1&b=0&i='
    get_data_url2 = 'http://members.tsetmc.com/tsev2/data/InstTradeHistory.aspx?i='
    get_data_url3 = '&Top=999999&A=0'
    try:
        row_data = requests.get(get_data_url + str(stock.tmc_id))
    except requests.HTTPError:
        return get_stock_history(stock)
    logger.info(str(stock) + ' logs fetched')
    stock_logs = row_data.text.split('\r\n')[1:]
    stock_logs = clean_stock_logs(stock_logs)
    return stock_logs
