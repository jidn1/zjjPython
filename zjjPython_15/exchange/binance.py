#!/usr/bin/python
from typing import Dict, Any

import requests
import json
import time
from datetime import datetime
from threading import Timer
import telegram


# 常量 设置监听的价格 和监听的交易对
wsSend = json.dumps({"method": "SUBSCRIBE", "params": ['!ticker@arr'], "id": 691})

dataList=[]


def handleTicker(ws,message):
    dataLine = json.loads(message)
    if 'ping' in dataLine:
        pong(ws)

    if len(dataList) > 0:
        print("dataList is full")
    else:
        if 'result' not in dataLine:
            tradeList = dataLine['data']
            for i in range(len(tradeList)):
                pricePercent = tradeList[i]['P']
                if float(pricePercent) > 30.0:
                    data = {}
                    data['s'] = tradeList[i]['s']
                    data['p'] = tradeList[i]['P']
                    data['v'] = tradeList[i]['v']
                    data['c'] = tradeList[i]['c']
                    dataList.append(data)
                    # print(str(dataList))
                    # msg = print_message(tradeList[i]['s'],tradeList[i]['P'],tradeList[i]['v'],tradeList[i]['c'])
                    # print(msg)
                    # print(pricePercent)


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


def bot_send(msg):
    bot = telegram.Bot(token='1868057848:AAGde8KxQSrOvEU4jfWOZ99lMnD8jcWu0G0')
    bot.sendMessage(chat_id='1617153685', text=msg)


def printTime(inc):
    msg = "币安目前24小时最新涨幅排行榜如下："
    msg_con = ""
    if len(dataList) > 0:
        for i in range(len(dataList)):
            msg_con = msg_con + "\n"+ dataList[i]['s']+","+dataList[i]['p'] +"%, "+dataList[i]['v']+", 最新价:"+dataList[i]['c']



    msg = msg + msg_con;
    # print(msg)
    bot_send(msg)
    t = Timer(inc, printTime, (inc,))
    t.start()
    dataList.clear()


