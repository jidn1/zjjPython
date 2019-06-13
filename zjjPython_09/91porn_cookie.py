#! zjjtv python
# -*- coding: utf-8 -*-
import requests
import os,re,time,random,threading

def Handler(start, end, url, filename):
    headers = {'Range': 'bytes=%d-%d' % (start, end)}
    with requests.get(url, headers=headers,stream=True) as r:
        with open(filename, "r+b") as fp:
            fp.seek(start)
            var = fp.tell()
            fp.write(r.content)
def download(url,tittle, num_thread = 10):
    r = requests.head(url)
    try:
        file_name = tittle
        file_size = int(r.headers['content-length'])
    except:
        print("检查URL，或不支持对线程下载")
        return
    fp = open(file_name, "wb")
    fp.truncate(file_size)
    fp.close()
    part = file_size // num_thread
    for i in range(num_thread):
        start = part * i
        if i == num_thread - 1:
            end = file_size
        else:
            end = start + part
        t = threading.Thread(target=Handler, kwargs={'start': start, 'end': end, 'url': url, 'filename': file_name})
        t.setDaemon(True)
        t.start()

    # 等待所有线程下载完成
    main_thread = threading.current_thread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        t.join()
    print('%s 下载完成' % file_name)


def random_ip():
    a=random.randint(1,255)
    b=random.randint(1,255)
    c=random.randint(1,255)
    d=random.randint(1,255)
    return(str(a)+'.'+str(b)+'.'+str(c)+'.'+str(d))
def get_cookie():
    with open('cookie.txt','r') as f:
        cookies={}
        for line in f.read().split(';'):
            name,value=line.strip().split('=',1)  #1代表只分割一次
            cookies[name]=value
        return cookies
flag=1
while flag<=100:
    tittle=[]
    base_url='http://91porn.com/view_video.php?viewkey='
    page_url='http://91porn.com/v.php?next=watch&page='+str(flag)
    get_page=requests.get(url=page_url)
    viewkey=re.findall(r'<a target=blank href="http://91porn.com/view_video.php\?viewkey=(.*)&page=.*&viewtype=basic&category=.*?">\n                    <img ',str(get_page.content,'utf-8',errors='ignore'))
    for key in viewkey:
        headers={'Accept-Language':'zh-CN,zh;q=0.9','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36','X-Forwarded-For':random_ip(),'referer':page_url,'Content-Type': 'multipart/form-data; session_language=cn_CN'}
        video_url=[]
        img_url=[]
        s = requests.Session()
        base_req=s.get(url=base_url+key,headers=headers,cookies=get_cookie(),verify=False)

        video_url=re.findall(r'<source src="(.*?)" type=\'video/mp4\'>',str(base_req.content,'utf-8',errors='ignore'))
        tittle=re.findall(r'<div id="viewvideo-title">(.*?)</div>',str(base_req.content,'utf-8',errors='ignore'),re.S)
        img_url=re.findall(r'poster="(.*?)"',str(base_req.content,'utf-8',errors='ignore'))
        try:
            t=tittle[0]
            tittle[0]=t.replace('\n','')
            t=tittle[0].replace(' ','')
        except IndexError:
            pass
        if os.path.exists(str(t))==False:
            try:
                download(str(video_url[0]),str(t)+'.mp4')
            except:
                pass
        else:
            print('已存在文件夹,跳过')
            time.sleep(2)
    flag=flag+1
    print('此页已下载完成，下一页是'+str(flag))