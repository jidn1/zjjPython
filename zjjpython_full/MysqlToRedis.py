#!/usr/bin/python
from util.myRedis import MyRedisPool
from util.mysql_DBUtil import MyPymysqlPool
import json
#获取mysql
mysql = MyPymysqlPool("dbMysql")

#获取Redis
redis = MyRedisPool("dbRedis")


if __name__ == '__main__':
    redis = MyRedisPool("dbRedis")
    news_param = {};
    news_param = redis.hget("wechat:voice","小吉")
    print(json.dumps(news_param,indent=4,sort_keys=True))
   # str = json.loads(news_param)
   # print(str)
   #  for k,v in news_param.items:
   #      print(k)



    # mysql = MyPymysqlPool("dbMysql")
    # sqlAll = "INSERT INTO novel (title, content) VALUES(%(title)s, %(content)s);"