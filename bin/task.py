#!/usr/bin/env python
#-*-coding:utf8-*-

import sys
sys.path.append('..')
import logging
import datetime
import os
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()

#读取配置信息
import json
BASEPATH = os.path.dirname(__file__)
stream = file(os.path.join(BASEPATH,'../config.json'), 'r')
config = json.load(stream)


@scheduler.scheduled_job("cron", hour=config['task']['updateRong360Rate']['hour'],minute=config['task']['updateRong360Rate']['minute'])
def updateRong360Rate():
    """
    更新rong360数据
    """
    os.system('scrapy crawl rong360')#执行爬虫命令
    
@scheduler.scheduled_job("cron", hour=config['task']['updateFangCommunity']['hour'],minute=config['task']['updateFangCommunity']['minute'])
def updateFangCommunity():
    """
    更新搜房网小区数据
    """
    os.system('scrapy crawl fang_community')#执行爬虫命令
    
@scheduler.scheduled_job("cron", hour=config['task']['updateNewHouse']['hour'],minute=config['task']['updateNewHouse']['minute'])
def updateNewHouse():
    """
    更新搜房网新房初始数据
    """
    os.system('scrapy crawl fang_newhouse')#执行爬虫命令
    
@scheduler.scheduled_job("cron", hour=config['task']['updateNewHouseDetail']['hour'],minute=config['task']['updateNewHouseDetail']['minute'])
def updateNewHouseDetail():
    """
    更新搜房网新房静态特征数据
    """
    os.system('scrapy crawl fang_communityDetail')#执行爬虫命令
    
@scheduler.scheduled_job("cron", hour=config['task']['updateNewHouseDynamic']['hour'],minute=config['task']['updateNewHouseDynamic']['minute'])
def updateNewHouseDynamic():
    """
    更新搜房网新房动态特征数据
    """
    os.system('scrapy crawl fang_newhouseDynamic')#执行爬虫命令



if __name__ == '__main__':
    try:
        print 'task start'
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
