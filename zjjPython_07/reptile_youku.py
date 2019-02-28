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
new_url = 'https://wangzhijiami.51240.com/'



# 写入数据库
def write_db(param):
    try:
        sql = "INSERT INTO `fh_movie` ( `moviceName`, `movicePictureUrl`, `movicePlayerUrl`, `country`, `language`, `mainCharacter`) "
        sql = sql + "VALUES(%(moviceName)s,%(movicePictureUrl)s,%(movicePlayerUrl)s,%(country)s,%(language)s,%(mainCharacter)s)"
        mysql.insert(sql, param)
        print("插入数据库")
    except Exception as e:
        print(e)


# 主方法
def main():
    global headers
    res = requests.get(new_url, headers=headers)
    html = res.content.decode('utf-8')#这里用utf-8解析
    Panelhtml = BeautifulSoup(html,'html.parser')#html.parser解析器
    moviePanel = Panelhtml.find('ul',class_="panel")
    #   print(moviePanel)
    movies = moviePanel.find_all('li',class_='yk-col4 mr1')
    # print("一共有"+movies+"部电影")
    for lis in movies:
        try:
            movie_param = {}
            #标题
            movicePictureUrl = lis.find('img',class_="quic").get("src");
            movicePlayerUrl = lis.find('ul',class_="info-list").find('li',class_="title").find("a").get("href");
            moviceName = lis.find('ul',class_="info-list").find('li',class_="title").find("a").get("title");
            mainCharacter = lis.find('ul',class_="info-list").find('li',class_="actor").find("a").get("title");
            mainCharacters = lis.find('ul',class_="info-list").find('li',class_="actor").find_all("a")[1].get("title");

            print(moviceName+""+mainCharacter+""+movicePictureUrl+""+movicePlayerUrl)

            movie_param['movicePictureUrl'] = movicePictureUrl
            movie_param['movicePlayerUrl'] = "https:"+movicePlayerUrl
            movie_param['moviceName'] = moviceName
            movie_param['mainCharacter'] = mainCharacter+","+mainCharacters
            movie_param['country'] = "美国"
            movie_param['language'] = "英语"
            write_db(movie_param)
        except Exception as e:
            print(e)

    mysql.end("commit")
    mysql.dispose()




if __name__ == '__main__':
    main()


