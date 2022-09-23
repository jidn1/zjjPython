#!/usr/bin/python
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import smtplib
from email.mime.text import MIMEText
import json
import matplotlib.pyplot as plt
import pandas as pd
import pytab as pt

global headers
headers = {
    'Accepts': 'application/json'
}

# 地址
# klineUrl = 'https://api.coinmarketcap.com/data-api/v3/exchange/market-pairs/latest'
cmc_url = 'https://api.coinmarketcap.com/data-api/v3/exchange/market-pairs/latest?slug=bitget&category=perpetual&start=1&limit=120'
payload = {
    # 'slug': 'bitget', 'category': 'spot', 'start': 0, 'limit': 181
}

spot_url = 'https://capi.bitget.bike/api/mix/v1/market/contracts?productType=umcbl'

spot_symbol = []
cmc_symbol = []


def getCMCSymbols():
    try:
        session = Session()
        session.headers.update(headers)
        response = session.get(cmc_url, params=payload)
        data = json.loads(response.text)
        for symbolInfo in data['data']['marketPairs']:
            symbol = symbolInfo['marketPair']
            cmc_symbol.append(symbol.replace("/", ""))
    except Exception as e:
        print(e)


def getBitGetSpotSymbols():
    try:
        session = Session()
        session.headers.update(headers)
        response = session.get(spot_url)
        data = json.loads(response.text)
        print(data)
        for symbolInfo in data['data']:
            spot_symbol.append(symbolInfo['symbol'].replace("_UMCBL", ""))
    except Exception as e:
        print(e)



def diff(bitgetSymbols,cmcSymbols):
    diffSymbols = list(set(bitgetSymbols).difference(set(cmcSymbols)))
    return diffSymbols


def getContent(symbols):
    html_text = '''
        <table border=1>
        <tr><th>S/N</th><th>FULL coin name</th><th>TICKER</th><th>Direct URL</th></tr>
       '''
    for s in symbols:
        sym = str(s)
        sym.endswith("USDT","")

        html_text = html_text + '<tr><td>'+s+'</td><td>'+s+'</td><td>'+s+'</td><td>https://www.bitget.com/en/trade/'+s+'</td></tr>'

    html_text = html_text + '''</table>'''
    return html_text


def sendEmail(title,receivers,content):
    # 常量
    mail_host = ""
    mail_user = ""
    mail_pass = ""
    sender = ''

    message = MIMEText(content, _subtype='html',_charset='utf-8')
    message['From'] = '比特吉'
    message['To'] = receivers
    message['Subject'] = title
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)


def table():
    data = {
        'Linux': [29, 23, 29, 20, 25, 23, 26],
        'LinuxMi': [26, 23, 29, 28, 20, 22, 29],
    }

    pt.table(
        data=data,
        th_type='dark',
        table_type='striped'
    )
    return pt;


if __name__ == '__main__':
    getCMCSymbols()
    getBitGetSpotSymbols()
    diffSymbols = diff(spot_symbol,cmc_symbol)
    # content = getContent(diffSymbols)
    print(diffSymbols)
    # content = table()
    # sendEmail('bitget-all-add cryptoasset','',content)

    # symbol= 'BTCUSDT'
    # print(symbol.replace('USDT',''))