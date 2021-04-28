#!/usr/bin/python
from websocket import create_connection
import json
import time


symbol = 'cmt_ethusdt'
websocketURL = 'ws://localhost:9999/websocket'
payload = json.dumps({'action': 'history', 'msgId': 'message1619590179968', 'productCode': symbol, 'size': 50})

getStartTime = "2021-04-28 16:02:00"
getEndTime = "2021-04-28 16:02:59"


def websocketReceived():
    ws = create_connection(websocketURL)
    ws.send(payload)
    flag = True
    KlineData = {}
    priceList = []
    sizeList = []
    while flag:
        result = ws.recv()
        dataLine = json.loads(result)
        historyData = {}
        if 'ifOrNotSuccess' not in dataLine:
            tradeList = dataLine['data']
            for i in range(len(tradeList)):
                time_local = time.localtime(int(tradeList[i][0])/1000)
                dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                if getStartTime <= dt <= getEndTime:
                    historyData['symbol'] = symbol
                    historyData['time'] = dt
                    historyData['price'] = tradeList[i][1]
                    historyData['size'] = tradeList[i][2]
                    print(historyData)
                    priceList.append(float(tradeList[i][1]))
                    sizeList.append(int(tradeList[i][2]))

                if dt > getEndTime:
                    flag = False
                    break;



    KlineData['symbol'] = symbol
    KlineData['time'] = getStartTime
    KlineData['open'] = priceList[0]
    KlineData['high'] = max(priceList)
    KlineData['low'] = min(priceList)
    KlineData['close'] = priceList[len(priceList) - 1]
    KlineData['volume'] = sum(sizeList)
    print(KlineData)
    ws.close()


if __name__ == '__main__':
    websocketReceived()