#!/usr/bin/python
import time
import pdfplumber
from baidu_api import baidu_api


class Pdf(baidu_api):

    def __init__(self, api_id, api_secret_key, from_lang='cht', to_lang='zh'):
        super(Pdf, self).__init__(api_id, api_secret_key, from_lang, to_lang)

    '''
     读取pdf 文件内容
    '''
    def read_pdf(self, url):
        words_list = []
        with pdfplumber.open(url) as pdf:
            first_page = pdf.pages[10]
            list_words = first_page.extract_text()
            print(list_words)
            for words in list_words:
                print(words['text'])
                time.sleep(1)
                res = super().translate(words['text'])
                print(res)
                words_list.append(res)


    '''
     读取图片
    '''
    def get_img(self, url):
        with pdfplumber.open(url) as pdf:
            # page = pdf.pages[155]
            for i, page in enumerate(pdf.pages):
                for img in page.images:
                    data = img['stream'].get_data()
                    super().pdf_ocr(data, i)

