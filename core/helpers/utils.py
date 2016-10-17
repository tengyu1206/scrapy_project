# -*- coding:utf-8 -*-
'''
常用工具包
'''
import chardet
import hashlib
import types
#判断网页的编码格式
def htmlcode(self,html):
        content=""
        mychar = chardet.detect(html)
        bianma = mychar['encoding']
        if bianma == 'utf-8' or bianma == 'UTF-8':
            content = html
        else:
            content = html.decode('gb2312','ignore').encode('utf-8')
        return content
#计算md5
def md5(str):
    if type(str) is types.StringType:
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest()
    else:
        print type(str)
