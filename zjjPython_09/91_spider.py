import requests
import os, re, time, random


def download_mp4(url, dir):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36Name',
        'Referer': 'http://91porn.com'}
    req = requests.get(url=url)
    filename = str(dir) + '/1.mp4'
    with open(filename, 'wb') as f:
        f.write(req.content)


def download_img(url, dir):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36Name',
        'Referer': 'http://91porn.com'}
    req = requests.get(url=url)
    with open(str(dir) + '/thumb.png', 'wb') as f:
        f.write(req.content)


def random_ip():
    a = random.randint(1, 255)
    b = random.randint(1, 255)
    c = random.randint(1, 255)
    d = random.randint(1, 255)
    return (str(a) + '.' + str(b) + '.' + str(c) + '.' + str(d))


flag = 1
while flag <= 100:
    tittle = []
    base_url = 'http://91porn.com/view_video.php?viewkey='
    page_url = 'http://91porn.com/v.php?next=watch&page=' + str(flag)
    get_page = requests.get(url=page_url)
    viewkey = re.findall('http://91porn.com/view_video.php\?viewkey=(.*?)&page=.*?&viewtype=basic&category=.*?" title=',
                         get_page.text)
    for key in viewkey:
        headers = {'Accept-Language': 'zh-CN,zh;q=0.9',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
                   'X-Forwarded-For': random_ip(), 'referer': page_url,
                   'Content-Type': 'multipart/form-data; session_language=cn_CN'}
        video_url = []
        base_req = requests.get(url=base_url + key, headers=headers)
        ifm = re.findall('<iframe width="560" height="315" src="(.*?)" frameborder="0" allowfullscreen></iframe>',
                         base_req.text)
        bases_req = requests.get(ifm[0], headers=headers)
        video_url = re.findall(r'<source src="(.*?)" type=\'video/mp4\'>',
                               str(bases_req.content, 'utf-8', errors='ignore'))
        tittle = re.findall(r'<div id="viewvideo-title">(.*?)</div>', str(base_req.content, 'utf-8', errors='ignore'),
                            re.S)
        try:
            t = tittle[0]
            tittle[0] = t.replace('\n', '')
            t = tittle[0].replace(' ', '')
        except Exception as e:
            print(e)
        uploadtime = re.findall(
            r'<span class="info">添加时间: </span>.*<span class="title">(\d\d\d\d-\d\d-\d\d)</span>',
            str(base_req.content, 'utf-8', errors='ignore'))  # 视频上传时间
        uploadtime_str = "".join(uploadtime)  # 视频上传时间
        savepath = "D:/91号店/" + uploadtime_str + str(t)  # 保存路径
        if os.path.exists(savepath) == False:
            try:
                os.makedirs(savepath)
                print('开始下载:' + str(t))
                download_mp4(str(video_url[0]), savepath)
                print('下载完成')
            except Exception as e:
                print(e)
        else:
            print('已存在文件夹,跳过')
            time.sleep(2)
    flag = flag + 1
    print('此页已下载完成，下一页是' + str(flag))
