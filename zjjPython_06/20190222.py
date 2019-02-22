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
        #print(html)  #错了就上这里看看
        url='https://'+url.split('/')[2]
        ts_file=parse_ts_2(html)
        print("**************")
        print(len(ts_file))
        print("**************")
        for i in range(len(ts_file)):
            #ts_file[i]=url+ts_file[i]+'.ts'
            #ts_file[i]=eec+ts_file[i]+'.ts'
            ts_file[i]=ts_file[i]+'.ts'
        print("例："+ts_file[0])
    except Exception:
        print('缓存文件请求错误2，请检查错误')
def parse_ts_2(html):
    global ts_num
    pattern=re.compile('.*?(.*?).ts')
    ts_lists=re.findall(pattern,html)
    ts_num=len(ts_lists)
    return(ts_lists)
ts_num=0
ts_file=[""]*2300
head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
url=sys.argv[1]
ls=len(sys.argv[1].split('/'))-1
ls2=len(sys.argv[1])-len(sys.argv[1].split('/')[ls])
eec=sys.argv[1][:ls2]
get_m3u8_2(url)

f=open("ts.txt","a+")
for i in range(0,ts_num):
    new_context =ts_file[i]+'\n'
    #    new_context ="file '"+ts_file[i]+"'\n"
    f.write(new_context)
f.close()