#!/usr/bin/python
import os
from urllib.request import urlretrieve
from multiprocessing import Pool
from datetime import datetime
import ssl


ssl._create_default_https_context = ssl._create_unverified_context
abc=[""]
down_num=0
for line in open("ts.txt"):
    #print(line, end = '') #这样不隔行
    abc.append(line[:-1])
for i in range(len(abc)-1):
    abc[i]=abc[i+1]
abc.pop()
num =len(abc[0].split('/')[len(abc[0].split('/'))-1][:-6])
def save_ts(a):
    global down_num
    try:
        b=a.split('/')[len(a.split('/'))-1]
        b=b[num:]
        if len(b)==6:
            b='0'+b
        urlretrieve(a,'hxjy/'+b)
        print(b)
        down_num+=1
    except Exception:
        print('保存有误:'+a)
print('正在下载...')
aa=datetime.now()
pool=Pool(16)
pool.map(save_ts,[a for a in abc])
pool.close()
pool.join()
bb=datetime.now()
print('下载完成')
print('用时 '+str((bb-aa).seconds)+' 秒')
L=[""]
i=0
for filename in os.listdir('/home/pi/Desktop/hxjy/'):
    L.append('hxjy/'+filename)
    L[i]=L[i+1]
    i+=1
L.pop()
print('共下载 '+str(len(L))+' 个文件')
print(down_num)