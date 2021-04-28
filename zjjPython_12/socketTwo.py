#!/usr/bin/python
import websocket
import json
import time
import constant as c


# 常量
symbol = 'cmt_ethusdt'
websocketURL = 'wss://localhost:9999/websocket'
payload = json.dumps({'action': 'history', 'msgId': 'message1619590179968', 'productCode': symbol, 'size': 50})
getStartTime = "2021-04-28 17:38:00"
getEndTime = "2021-04-28 17:38:59"

# 定义 list
KlineData = {}
priceList = []
sizeList = []


def buildBar():
    KlineData['symbol'] = symbol
    KlineData['time'] = getStartTime
    KlineData['open'] = priceList[0]
    KlineData['high'] = max(priceList)
    KlineData['low'] = min(priceList)
    KlineData['close'] = priceList[len(priceList) - 1]
    KlineData['volume'] = sum(sizeList)
    print(KlineData)


def handle(ws,messgae):
    dataLine = json.loads(messgae)
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


def on_message(ws, message):
    handle(ws,message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")
    ws.close()


def on_open(ws):
    ws.send(c.payload)


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

