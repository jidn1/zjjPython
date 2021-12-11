#!/usr/bin/python
import json
import time
import threading
import utils.email_util as sendE


# 常量 设置监听的价格 和监听的交易对
setPrice = 0.00003451
symbol = "shibusdt"
wsSend = json.dumps({"method": "SUBSCRIBE", "params": ['!miniTicker@arr'], "id": 691})
receivers = 'ji.dening@upex.co'

def handleTicker(ws,message):
    dataLine = json.loads(message)
    print(dataLine)
    if 'ping' in dataLine:
        pong(ws)

    if 'result' not in dataLine:
        print(dataLine['data'])
        price = float(dataLine['data']['c'])
        quoteChange = float(dataLine['data']['P'])
        t = threading.Thread(target= match_price, args=(price,quoteChange), name='match_price');
        t.start()
        t.join()


def on_message(ws, message):
    handleTicker(ws,message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")
    ws.close()


def on_open(ws):
    ws.send(wsSend)


def pong(ws):
    pongStr = json.dumps({"pong": int(round(time.time() * 1000))})
    ws.send(pongStr)


def match_price(price,quoteChange):
    print("binance btc_usdt last price:"+str(price)+", 24h quote change is:"+str(quoteChange)+"%")


def send_email_huobi(price):
    content = '您好，您关注的币安平台'+symbol+',已低于您设置的: '+str(setPrice)+'价格，目前最新价格为:'+str(price)+',上次设置已失效，如需再次提醒，请重新设置价格'
    sendE.sendEmail('比特吉行情提醒',receivers,content)