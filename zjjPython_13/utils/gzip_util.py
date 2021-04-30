#!/usr/bin/python
import gzip


# 解压
def Gz_Decode(data):
    return gzip.decompress(data).decode('utf8')


# 压缩
def Gz_Encode(data):
    if type(data) == str:
        data = bytes(data, 'utf8')
    s_out = gzip.compress(data)
    return s_out