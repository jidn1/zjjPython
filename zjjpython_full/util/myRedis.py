#!/usr/bin/python
# 导入redis模块
import redis
import configparser
import os
import json

class Config(object):

    def __init__(self, config_filename="dbMyRedisConfig.cnf"):
        file_path = os.path.join(os.path.dirname(__file__), config_filename)
        self.cf = configparser.ConfigParser()
        self.cf.read(file_path)

    def get_sections(self):
        return self.cf.sections()

    def get_options(self, section):
        return self.cf.options(section)

    def get_content(self, section):
        result = {}
        for option in self.get_options(section):
            value = self.cf.get(section, option)
            result[option] = int(value) if value.isdigit() else value
        return result

class BaseRedisPool(object):
    def __init__(self, host, port, password, db_name):
        self.db_host = host
        self.db_port = int(port)
        self.password = str(password)
        self.db = db_name
        self.r = None
        self.pipe = None

class MyRedisPool(BaseRedisPool):
    # 连接池对象
    __pool = None

    def __init__(self, conf_name=None):
        self.conf = Config().get_content(conf_name)
        super(MyRedisPool, self).__init__(**self.conf)
        # 数据库构造函数，从连接池中取出连接，并生成操作游标
        if MyRedisPool.__pool is None:
            __pool = redis.ConnectionPool(
            host=self.db_host,
            port=self.db_port,
            password=self.password,
            db=self.db,
            decode_responses=True)
            self.r = redis.Redis(connection_pool=__pool)
            self.pipe = self.r.pipeline()



    def set(self,key,values=None):
        try:
            return self.r.set(key,values)
        except Exception as e:
            print(e)

    def get(self,key):
        try:
            return self.pipe.get(key)
        except  Exception as e:
            print(e)

    def hset(self,name,key,value):
        try:
            self.pipe.hset(name,key,value)
            return  self.pipe.execute()
        except Exception as e:
            print(e)

    def hget(self,name,key):
        try:
            return self.pipe.hget(name,key).execute()
        except Exception as e:
            print(e)

    def hgetAll(self,name):
        try:
            return self.pipe.hgetall(name).execute()
        except Exception as e:
            print(e)

    def delete(self,name):
        try:
            self.pipe.delete(name)
            self.pipe.execute()
        except Exception as e:
            print(e)

    def hdel(self,name,key):
        try:
            self.pipe.hdel(name,key)
            self.pipe.execute()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    #redis = MyRedisPool("dbRedis")
   # name = redis.hget("config","name")
   # print(str(name))
    list_param =[]

    news_param = {}
    news_param['newTitle'] = "7018米！中国科学家又迎来历史性突破"
    news_param['newImg'] = "http://p0.ifengimg.com/pmop/2018/0604/A86C60F870F57DC844F85DB58AD1A643561A4B6BA_size36_w640_h431.jpeg"
    news_param['newHref'] = "http://news.ifeng.com/a/20180604/58565046_0.shtml"
    news_param['newType'] = "资讯排行"

    news_param1 = {}
    news_param1['newTitle'] = "7018米！中国科学家又迎来历史性突破"
    news_param1['newImg'] = "http://p0.ifengimg.com/pmop/2018/0604/A86C60F870F57DC844F85DB58AD1A643561A4B6BA_size36_w640_h431.jpeg"
    news_param1['newHref'] = "http://news.ifeng.com/a/20180604/58565046_0.shtml"
    news_param1['newType'] = "资讯排行"

    list_param.append(news_param)
    list_param.append(news_param1)
   # print(news_param["newType"])
    json_str = json.dumps(list_param,ensure_ascii=False)
    print(json_str)
