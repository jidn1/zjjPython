#!/usr/bin/python
import requests
import json
import time


global headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}

# 地址
klineUrl = 'https://capi.bitget.bike/api/tv/v3/history'
payload = {'symbol': 'cmt_ethusdt', 'resolution': '1', 'from': 0, 'to': 0}

streamingUrl = 'https://capi.bitget.bike/api/tv/v3/streaming'
filterSymbol = 'ETHUSDTPERP'
getStartTime = "2021-04-30 16:12:00"
getEndTime = "2021-04-30 16:12:59"


def tradingViewStreaming():
    res = requests.get(streamingUrl, stream=True, headers=headers)
    if res.encoding is None:
        res.encoding = 'utf-8'

    KlineData = {}
    priceList = []
    sizeList = []
    try:
        for line in res.iter_lines(decode_unicode=True):
            if line:
                data = json.loads(line)
                if data['f'] == 't' and data['id'] == filterSymbol:
                    timestamp = data['t']
                    time_local = time.localtime(timestamp)
                    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                    if getStartTime <= dt <= getEndTime:
                        size = data['s']
                        price = data['p']
                        priceList.append(price)
                        sizeList.append(size)
                        print(data)

                    if dt > getEndTime:
                        break;
    except Exception as e:
        print(e)

    KlineData['symbol'] = filterSymbol
    KlineData['time'] = getStartTime
    KlineData['open'] = priceList[0]
    KlineData['high'] = max(priceList)
    KlineData['low'] = min(priceList)
    KlineData['close'] = priceList[len(priceList) - 1]
    KlineData['volume'] = sum(sizeList)
    print(KlineData)


def getKlineData():
    try:
        startArray = time.strptime(getStartTime, "%Y-%m-%d %H:%M:%S")
        startTime = time.mktime(startArray)
        endArray = time.strptime(getEndTime, "%Y-%m-%d %H:%M:%S")
        endTime = time.mktime(endArray)
        payload['from'] = int(startTime)
        payload['to'] = int(endTime)
        res = requests.get(klineUrl, params=payload, headers=headers)
        print(res.json())
    except Exception as e:
        print(e)


if __name__ == '__main__':
    tradingViewStreaming()
    getKlineData()
