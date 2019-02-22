#!/usr/bin/python
import os
from datetime import datetime


L=[""]
i=0
for filename in os.listdir('/home/pi/Desktop/hxjy/'):
    L.append('hxjy/'+filename)
    L[i]=L[i+1]
    i+=1
L.pop()
L.sort()
f=open("txsp.txt","a+")
for i in range(0,len(L)):
    new_context ="file '"+L[i]+"'\n"
    if (i==len(L)-1):
        f.write(new_context[:-1])
    else:
        f.write(new_context)
f.close()
aa=datetime.now()
tt=datetime.now().strftime('%Y%m%d%H%M%S')
os.system("sudo ffmpeg -f concat -i txsp.txt -c copy api/share/"+tt+".mkv")
bb=datetime.now()
print((bb-aa).seconds)
os.system("sudo rm hxjy/*.ts")
os.system("sudo rm ts.txt")
os.system("sudo rm txsp.txt")
os.system("omxplayer api/share/"+tt+".mkv")