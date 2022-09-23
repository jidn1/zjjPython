#!/usr/bin/python
import requests
import telegram
from bs4 import BeautifulSoup
from requests import Session
import json, time
from contants import *

binance_announcement_url = 'https://www.binance.com/zh-CN/support/announcement/'
announcement_list_url = "https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=1&pageNo=1&pageSize=50"
global headers
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36','lang': 'zh-CN'}


def getBinanceAnnouncement(url):
    try:
        response = requests.get(url, headers=headers)
        response_html = response.content.decode('utf-8')
        html = BeautifulSoup(response_html, 'html.parser')
        content = html.find_all('meta')[2].get('content')
        return content
    except Exception as e:
        print(e)


def getAnnouncementList():
    try:
        session = Session()
        session.headers.update(headers)
        response = session.get(announcement_list_url)
        data = json.loads(response.text)
        spot = data['data']['catalogs'][0]

        title = spot['articles'][0]['title']
        code = spot['articles'][0]['code']
        release_time = spot['articles'][0]['releaseDate']
        time_local = time.localtime(release_time/1000)
        releaseDate = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        url = getContentUrl(code)
        content = getBinanceAnnouncement(url)

        msg = getTip(title,content,releaseDate,url)
        bot = telegram.Bot(token=bot_token)
        bot.send_message(chat_id=group_id, text=msg, parse_mode='markdown')
    except Exception as e:
        print(e)


def getContentUrl(code):
    return binance_announcement_url + str(code)


def getTip(title,content,releaseDate,url):
    return "币安上币公告：\n {title}\n {content} \n {releaseDate} \n [点击查看]({url})".format(title=title,content=content,releaseDate=releaseDate,url=url)



if __name__ == '__main__':
    getAnnouncementList()