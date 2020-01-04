#!/usr/bin/python
import requests
from bs4 import BeautifulSoup
import redis
import time,datetime
import pymysql

# 请求头
global headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}


#redis
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password='Credit2016Admin',db=0)
r = redis.Redis(connection_pool=pool)

#mysql
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='video')
cursor = conn.cursor()


def main():
    crawler = r.get('crawUrl');
    crawlerStr = str(crawler);
    str1 = str(crawlerStr[crawlerStr.find("httpApi")+11:crawlerStr.find("httpApi")+32]);
    print('只爬取500页 start...')
    for i in range(50):
        print('第'+str(i)+'页开始')
        new_url = str1+'?ac=videolist&t=all&pg='+str(i);
        global headers
        res = requests.get(new_url, headers=headers)
        html = res.content.decode('utf-8')  # 这里用utf-8解析
        div_bf = BeautifulSoup(html, 'html.parser')  # html.parser解析器
        videos = div_bf.find_all('video')  # 筛选所有video标

        for v in videos:
            try:
                news_param = {}
                # 标题
                id = v.find('id').text
                name = v.find('name').text
                types = v.find('type').text
                pic = v.find('pic').text
                m3u8 = v.find('dl').find('dd').text
                last = v.find('last').text

                news_param['id'] = id
                news_param['name'] = name
                news_param['types'] = types
                news_param['picture'] = pic
                news_param['m3u8'] = m3u8
                news_param['last'] = last
                news_param['fire'] = id
                news_param['created'] = int(time.time())
                news_param['modified'] = int(time.time())

                r.lpush("video:porn:list",str(news_param))

                news_param['created'] = datetime.datetime.now()
                news_param['modified'] = datetime.datetime.now()
                sql = "INSERT INTO fh_porn_hub(name, type, picture, m3u8, fire, last, created, modified) VALUES " \
                      "(%(name)s,  %(types)s, %(picture)s, %(m3u8)s, %(fire)s, %(last)s,%(created)s, %(modified)s )";

                cursor.execute(sql,news_param)
                conn.commit()
            except Exception as e:
                print(e)

    cursor.close()
    conn.close()


if __name__ == '__main__':
    main()
