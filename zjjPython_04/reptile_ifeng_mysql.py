#!/usr/bin/python
# 导入requests库
import requests
# 导入文件操作库
import os
import re
import bs4
from bs4 import BeautifulSoup
import sys
from util.mysql_DBUtil import MyPymysqlPool


# 给请求指定一个请求头来模拟chrome浏览器
global headers
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
#获取mysql
mysql = MyPymysqlPool("dbMysql")
# 爬取地址
new_url = 'http://news.ifeng.com/hotnews/'



# 写入数据库
def write_db(param):
    try:
        sql = "insert into zjj_new (new_title,new_img,new_href,new_type) "
        sql = sql + "VALUES(%(new_title)s,%(new_img)s,%(new_href)s,%(new_type)s)"
        mysql.insert(sql, param)
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
        print(new_type)
        first_new = first.find_all('div',class_='tab_01')[0].find_all('tr')
        for trs in first_new:
            try:
                news_param = {}
                #标题
                new_title = trs.find_all('td')[1].text
                new_href = trs.find_all('td')[1].find('a').get("href")
                new_img = thumbnail(new_href)

                news_param['new_title'] = new_title
                news_param['new_img'] = new_img
                news_param['new_href'] = new_href
                news_param['new_type'] = new_type
                write_db(news_param)
            except Exception as e:
                print(e)

    mysql.end("commit")
    mysql.dispose()


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



if __name__ == '__main__':
    main()


