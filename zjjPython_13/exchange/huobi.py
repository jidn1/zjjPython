#!/usr/bin/python
import json
import time
import threading
import utils.email_util as sendE
import utils.gzip_util as g

# 常量 设置监听的价格 和监听的交易对
setPrice = 0.000028
symbol = "shibusdt"
wsSend = json.dumps({"sub": "market."+symbol+".detail", "symbol": symbol, "id": "huobiv"})
receivers = ''


def handleTicker(ws,message):
    dataLine = json.loads(message)
    if 'ping' in dataLine:
        pong(ws)

    if 'ch' in dataLine:
        price = float(dataLine['tick']['close'])
        t = threading.Thread(target= match_price, args=(price,ws), name='match_price');
        t.start()
        t.join()


def on_message(ws, message):
    msg = g.Gz_Decode(message);
    handleTicker(ws,msg)


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


def match_price(price,ws):
    print(symbol+'--'+'%.7f' % price)
    # if price > setPrice:
    #     # send_email_huobi(price)
    #     on_close(ws)



def send_email_huobi(price):
    content = '您好，您关注的火币平台'+symbol+',已低于您设置的: '+str(setPrice)+'价格，目前最新价格为:'+str(price)+',上次设置已失效，如需再次提醒，请重新设置价格'
    sendE.sendEmail('比特吉行情提醒',receivers,content)