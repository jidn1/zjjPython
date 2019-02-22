#!/usr/bin/python

import requests
import re,sys


def get_m3u8_1(url):
    try:
        response=requests.get(url,headers=head)
        html=response.text
        return html
    except Exception:
        print('缓存文件请求错误1，请检查错误')

def get_m3u8_2(url):
    global ts_file
    try:
        response=requests.get(url,headers=head)
        html=response.text
        #print(html)
        url='https://'+url.split('/')[2]
        ts_file=parse_ts_2(html)
        print("**************")
        print(len(ts_file))
        #for j in range(5000-len(ts_file)):
        #   ts_file.pop(len(ts_file))
        print("**************")
        for i in range(len(ts_file)):
            ts_file[i]=url+ts_file[i]+'.ts'
        print("例："+ts_file[0])
        print(url)
    except Exception:
        print('缓存文件请求错误2，请检查错误')
def parse_ts_2(html):
    global ts_num
    pattern=re.compile('.*?(.*?).ts')
    ts_lists=re.findall(pattern,html)
    ts_num=len(ts_lists)
    return(ts_lists)
ts_num=0
ts_file=[""]*5000
head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
url='https://www.hongxinhuaxue.com/20190210/TZuTlSlk/index.m3u8'
#url=sys.argv[1]
html=get_m3u8_1(url).strip()
print(html) #调整试试
url='https://'+url.split('/')[2] #父母爱情要取消这句
print(url)
url_2=url+html.split()[2]
#url_2=url[:-10]+html.split()[2] #父母爱情
get_m3u8_2(url_2)

f=open("ts.txt","a+")
for i in range(0,ts_num):   #2268是因为前面是1，所以要在数字基础上加1，而L[0]在这里实际为空！！
    new_context =ts_file[i]+'\n'
    #    new_context ="file '"+ts_file[i]+"'\n"
    f.write(new_context)
f.close()