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
new_url = 'https://list.youku.com/category/show/c_96_a_美国_u_1_pt_2_s_6_d_1_p_1.html'

page_url = 'https://list.youku.com/category/show/c_96_a_美国_u_1_pt_2_s_6_d_1_p_'



# 写入数据库
def write_db(param):
    try:
        sql = "INSERT INTO `fh_movie` ( `moviceName`, `movicePictureUrl`, `movicePlayerUrl`, `country`, `language`, `mainCharacter`,moviceReleaseTime) "
        sql = sql + "VALUES(%(moviceName)s,%(movicePictureUrl)s,%(movicePlayerUrl)s,%(country)s,%(language)s,%(mainCharacter)s,%(moviceReleaseTime)s)"
        mysql.insert(sql, param)
        print("插入数据库")
    except Exception as e:
        print(e)


# 爬取信息
def video(page_no):
    global headers
    res_sub = requests.get(page_no, headers=headers)
    video_html = res_sub.content.decode('utf-8')#这里用utf-8解析
    # 解析html
    Panelhtml = BeautifulSoup(video_html, 'html.parser')
    moviePanel = Panelhtml.find('ul',class_="panel")
    movies = moviePanel.find_all('li',class_='yk-col4 mr1')

    for lis in movies:
        try:
            movie_param = {}
            #
            movicePictureUrl = lis.find('img',class_="quic").get("src");
            movicePlayerUrl = lis.find('ul',class_="info-list").find('li',class_="title").find("a").get("href");
            moviceName = lis.find('ul',class_="info-list").find('li',class_="title").find("a").get("title");
            mainCharacter = lis.find('ul',class_="info-list").find('li',class_="actor").find("a").get("title");
            mainCharacters = lis.find('ul',class_="info-list").find('li',class_="actor").find_all("a")[1].get("title");
            moviceReleaseTime = lis.find('ul',class_="info-list").find_all('li')[2].text;

            moviceReleaseTime = moviceReleaseTime.replace("最近更新：","");

            print(moviceName+""+mainCharacter+""+movicePictureUrl+""+movicePlayerUrl)

            movie_param['movicePictureUrl'] = movicePictureUrl
            movie_param['movicePlayerUrl'] = "https:"+movicePlayerUrl
            movie_param['moviceName'] = moviceName
            movie_param['mainCharacter'] = mainCharacter+","+mainCharacters
            movie_param['country'] = "美国"
            movie_param['language'] = "英语"
            movie_param['moviceReleaseTime'] = moviceReleaseTime
            write_db(movie_param)
        except Exception as e:
            print(e)






# 主方法
def main():
    global headers
    res = requests.get(new_url, headers=headers)
    html = res.content.decode('utf-8')#这里用utf-8解析
    Panelhtml = BeautifulSoup(html,'html.parser')#html.parser解析器
    pageSize = Panelhtml.find('ul',class_="yk-pages").find_all("li")[6].find("a").text;
    print("总页数:"+pageSize)

    for i in range(1, int(pageSize) + 1):
        if i == 1:
            page = new_url
        else:
            page = page_url + str(i) + ".html"

        # 爬取电影页码
        print("页码：" + page)
        video(page)


    mysql.end("commit")
    mysql.dispose()



if __name__ == '__main__':
    main()


