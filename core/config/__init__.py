#!/usr/bin/env python
#-*-coding:utf8-*-
"""
主要是读取配置文件信息
"""
import yaml
import os
BASEPATH = os.path.dirname(__file__)
#读取数据库的配置
def dbConfig():
    stream = file(os.path.join(BASEPATH,'db.yaml'), 'r')
    dicts = yaml.load(stream)
    return dicts
#读取API地址的配置
def apiConfig(name):
    stream = file(os.path.join(BASEPATH,'api.yaml'), 'r')
    dicts = yaml.load(stream)
    return dicts[name]#返回指定名字的参数


if __name__ == '__main__':
    print apiConfig('eia')['url']
