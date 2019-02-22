#!/usr/bin/python

import requests,sys
import re,sys
from pyquery import PyQuery as pq


url_m3u8=""
def get_page(get_url):
    try:
        print('正在请求目标网页....')
        response=requests.get(get_url,headers=head)
        if response.status_code==200:
            head['referer'] = get_url
            return response.text
    except Exception:
        print('请求目标网页失败，请检查错误重试')
        return None

def parse_page(html):
    global url_m3u8
    print('目标信息正在解析........')
    doc=pq(html)
    #print(doc)
    title=doc('head title').text()
    print("目标视频为： "+title)
    url_m3u8 = doc('#player').attr('src')[14:]
    print(url_m3u8)


head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
#url=sys.argv[1]
url='https://v.qq.com/x/cover/gk11svuomdpsgl4.html' #火星任务
get_url = 'https://jx.618g.com/?url=' + url
html = get_page(get_url)
if html:
    parse_page(html)