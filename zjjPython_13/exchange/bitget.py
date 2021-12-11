#!/usr/bin/python
import json
import time
import threading
import utils.email_util as sendE
import utils.gzip_util as g


setPrice = 10.21
wsSend = json.dumps({"action": "all_ticker", "id": "all_ticker|btc_usdt"})

def handleTicker(ws,message):
    dataLine = json.loads(message)
    if 'ping' in dataLine:
        pong(ws)

    if 'ch' in dataLine:
        price = float(dataLine['tick']['close'])
        t = threading.Thread(target= match_price, args=(price,), name='match_price');
        t.start()
        t.join()


def on_message(ws, message):
    print(message)


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


def match_price(price):
    print(str(price)+'--'+threading.current_thread().name)
    if price < setPrice:
        send_email_huobi(price)



def send_email_huobi(price):
    content = '您好，您关注的火币平台EOS,已低于您设置的: '+setPrice+'价格，目前最新价格为:'+price+',上次设置已失效，如需再次提醒，请重新设置价格'
    sendE.sendEmail('比特吉行情提醒','',content)