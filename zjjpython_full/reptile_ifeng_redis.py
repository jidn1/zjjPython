#!/usr/bin/python
# 导入requests库
import requests
# 导入文件操作库
import os
import re
import bs4
import json
from bs4 import BeautifulSoup
import sys
from util.myRedis import MyRedisPool


# 给请求指定一个请求头来模拟chrome浏览器
global headers
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
#获取Redis
redis = MyRedisPool("dbRedis")
# 爬取地址
new_url = 'http://news.ifeng.com/hotnews/'



# 写入redis
def write_redis(newsType,param):
    try:
        json_str = json.dumps(param,ensure_ascii=False)
        redis.hset("wechat:news",newsType,json_str)
    except Exception as e:
        print(e)


# 主方法
def main():
    global headers
    res = requests.get(new_url, headers=headers)
    html = res.content.decode('utf-8')#这里用utf-8解析
    div_bf = BeautifulSoup(html,'html.parser')#html.parser解析器
    new = div_bf.find_all('div',class_='boxTab clearfix')#筛选所有div标

    for div_new in new:
        first = BeautifulSoup(str(div_new),'html.parser')
        new_type = first.find('span').text
        first_new = first.find_all('div',class_='tab_01')[0].find_all('tr')
        list_param =[]
        for trs in first_new:
            try:
                news_param = {}
                #标题
                new_title = trs.find_all('td')[1].text
                new_href = trs.find_all('td')[1].find('a').get("href")
                new_img = thumbnail(new_href)
                #new_introdu = introduction(new_href)
                news_param['newTitle'] = new_title
                news_param['newImg'] = new_img
                news_param['newHref'] = new_href
                news_param['newType'] = new_type
                #news_param['newIntroduction'] = new_introdu
                list_param.append(news_param)
            except Exception as e:
                print(e)

            write_redis(new_type,list_param)




def thumbnail(new_href):
    global headers
    res = requests.get(new_href, headers=headers)
    html = res.content.decode('utf-8')
    div_bf = BeautifulSoup(html,'html.parser')
    new = div_bf.find_all('p',class_='detailPic')
    if new.__len__() > 0 :
        img_url = new[0].find('img').get('src')
    else:
        img_url = ''

    return img_url



def introduction(new_href):
    global headers
    res = requests.get(new_href, headers=headers)
    html = res.content.decode('utf-8')
    div_bf = BeautifulSoup(html,'html.parser')
    newIntr = div_bf.find_all('div',class_='js_selection_area').find_all('p')[0].text
    if newIntr.__len__() > 4:
        new_intro = newIntr
    else:
        new_intro = div_bf.find_all('p',class_='photoDesc').text

    print(new_intro)
    return new_intro






if __name__ == '__main__':
    main()


