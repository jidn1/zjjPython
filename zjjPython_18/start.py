#!/usr/bin/python
import pdf as pdf_api
import baidu_api as baidu

if __name__ == '__main__':
    api_key = ""
    secret_key = ""
    url = input('请输入文件名字(文件应和本脚本放在同一目录下，否则无法转换):')

    PdfApi = pdf_api.Pdf(api_key, secret_key)
    PdfApi.get_img(url)

