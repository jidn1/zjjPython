#!/usr/bin/python
import requests


global headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}


tickerUrl = 'https://api.huobi.pro/market/detail/merged'


def getTicker(symbol):
    payload = {'symbol': symbol}
    res = requests.get(tickerUrl, params=payload, headers=headers)
    data = res.json()
    return priceHtml(symbol, data['tick']['close'], data['tick']['high'], data['tick']['low'])


def priceHtml(symbol, price, high, low):
    return '*Token*:' + symbol + \
           '\n*Price*: ' + str('%.8f' % price) + \
           '\n*High*: ' + str('%.8f' % high) + \
           '\n*Low*: ' + str('%.8f' % low);


if __name__ == '__main__':
    getTicker('shibusdt')