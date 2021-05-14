#!/usr/bin/python
import websocket
import json
import time
import requests
import constant as c


# 常量
global headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}

klineUrl = 'https://capi.bitget.bike/api/tv/v3/history'
klineParam = {'symbol': 'cmt_ethusdt', 'resolution': '1', 'from': 0, 'to': 0}


symbol = 'sbtcusd'
websocketURL = 'wss://contractsocket-ucloud.9ibp.com/websocket'
payload = json.dumps({'action': 'history', 'msgId': 'message1619609953328', 'productCode': symbol, 'size': 50})
klineSend = json.dumps({"action":"kline","productCode":"sbtcusd","step":"60","type":[1],"klineType":1,"msgId":"message1619690963671"})
getStartTime = "2021-04-29 19:27:00"
getEndTime = "2021-04-29 19:27:59"

# 定义 list
KlineData = {}
priceList = []
sizeList = []

lastN = 0


def getKlineData():
    try:
        startArray = time.strptime(getStartTime, "%Y-%m-%d %H:%M:%S")
        startTime = time.mktime(startArray)
        endArray = time.strptime(getEndTime, "%Y-%m-%d %H:%M:%S")
        endTime = time.mktime(endArray)
        klineParam['from'] = int(startTime)
        klineParam['to'] = int(endTime)
        res = requests.get(klineUrl, params=klineParam, headers=headers)
        print(res.json())
    except Exception as e:
        print(e)


def buildBar():
    KlineData['symbol'] = symbol
    KlineData['time'] = getStartTime
    KlineData['open'] = priceList[0]
    KlineData['high'] = max(priceList)
    KlineData['low'] = min(priceList)
    KlineData['close'] = priceList[len(priceList) - 1]
    KlineData['volume'] = sum(sizeList)
    print(KlineData)


def handleHistory(ws,dataLine):
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
                on_close(ws);
                break;


def handleKline(ws,dataLine):
    Kline = {}

    if 'ifOrNotSuccess' not in dataLine:
        if False == dataLine['first']:
            print(dataLine)
            tradeList = dataLine['data']

            for i in range(len(tradeList)):
                time_local = time.localtime(int(tradeList[i][5])/1000)
                dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                if getStartTime <= dt <= getEndTime:
                    Kline['symbol'] = symbol
                    Kline['time'] = dt
                    Kline['price'] = tradeList[i][1]
                    global lastN

                    newSize = int(tradeList[i][4]) - lastN
                    lastN = int(tradeList[i][4])

                    Kline['size'] = newSize
                    print(Kline)
                    priceList.append(float(tradeList[i][1]))
                    sizeList.append(int(lastN))

                if dt > getEndTime:
                    on_close(ws);
                    break;


def on_message(ws, message):
    dataLine = json.loads(message)
    if 'history' in dataLine['action']:
        handleHistory(ws,dataLine)
    else:
        handleKline(ws,dataLine)



def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")
    ws.close()


def on_open(ws):
    ws.send(klineSend)


def mainServer():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(c.websocketURL,
                                on_open = on_open,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)

    ws.run_forever()


if __name__ == "__main__":
    mainServer()
    buildBar()
    # getKlineData()

