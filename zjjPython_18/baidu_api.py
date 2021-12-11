#!/usr/bin/python
import http.client
import hashlib
import urllib
import random
import json
from aip import AipOcr

class baidu_api:
    def __init__(self,  api_id, api_secret_key, from_lang, to_lang):
        self.__api_id = api_id
        self.__api_secret_key = api_secret_key
        self.__from_lang = from_lang
        self.__to_lang = to_lang
        self.httpClient = None

    def get_url(self, txt):
        salt = random.randint(32768, 65536)
        sign = self.__api_id + txt + str(salt) + self.__api_secret_key
        sign = hashlib.md5(sign.encode()).hexdigest()
        return '/api/trans/vip/translate?appid=' + self.__api_id + '&q=' + urllib.parse.quote(txt) + '&from=' + self.__from_lang + '&to=' + self.__to_lang + '&salt=' +\
               str(salt) + '&sign=' + sign

    def translate(self, txt):
        try:
            self.httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            self.httpClient.request('GET', self.get_url(txt))
            response = self.httpClient.getresponse()
            result_all = response.read().decode("utf-8")
            result = json.loads(result_all)
            return result['trans_result'][0]['dst']
        except Exception as e:
            print(e)
        finally:
            if self.httpClient:
                self.httpClient.close()

    def pdf_ocr(self, img_data, page):
        words_list = []
        client = AipOcr('', '', '')
        # 调用百度API通用文字识别，提取图片中的内容
        text = client.basicAccurate(img_data)
        result = text["words_result"]
        for i in result:
            text = self.translate(i["words"])
            words_list.append(text)

        self.write_file(words_list, page)


    '''
     
    '''
    def write_file(self, words, page):
        file_name = '/Users/jidening/soft/doc/book/data_'+str(page)+'.txt'
        with open(file_name, 'w', encoding="utf-8") as f:
            for word in words:
                f.write(str(word))

            f.close()