#!/usr/bin/python
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
new_url = 'http://bddn.cn/zb.htm'



# 写入redis
def write_redis(tvName,tvHref):
    try:
        redis.hset("wechat:tv",tvName,tvHref)
    except Exception as e:
        print(e)


# 主方法
def main():
    global headers
    res = requests.get(new_url, headers=headers)
    html = res.content.decode('gb2312')
    table_all = BeautifulSoup(html,'html.parser')#html.parser解析器
    tables = table_all.find_all("a",attrs={'target':'_blank'})#筛选所有div标
    list_param =[]
    for tv in tables:
        if tv.text.__len__() > 0:
            write_redis(tv.text.replace(' ', ''),tv.get("href"))





if __name__ == '__main__':
    main()