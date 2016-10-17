# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Rong360Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()   
    #银行名称
    title = scrapy.Field()
    #支持类型：新房二手房
    #support_type = scrapy.Field()
    #url+title+today 组成的随机id
    rid = scrapy.Field()
    #城市中文名字
    cityName = scrapy.Field()    
    #审批时间
    examine_time = scrapy.Field()
    #放款时间
    loan_time = scrapy.Field()
    #url
    url = scrapy.Field()
    
    #type1首套住宅 discount
    type1_discount = scrapy.Field()
    #type1 rate
    type1_rate = scrapy.Field()
    #type1 first_pay
    type1_firstpay = scrapy.Field()
    
    #type2二套住宅 discount
    type2_discount = scrapy.Field()
    #type2 rate
    type2_rate = scrapy.Field()
    #type2 first_pay
    type2_firstpay = scrapy.Field()
    
    #type3商用房产 discount
    type3_discount = scrapy.Field()
    #type3 rate
    type3_rate = scrapy.Field()
    #type3 first_pay
    type3_firstpay = scrapy.Field()
    
    #datetime
    inserttime = scrapy.Field()


class FangCommunityItem(scrapy.Item):
    #url+title+today 组成的随机id
    rid = scrapy.Field()
    #城市名称
    cityName = scrapy.Field()
    #小区名称
    communityName = scrapy.Field()
    #小区url
    communityUrl = scrapy.Field()
    #小区别名
    aliasCommunity = scrapy.Field()
    #小区所在区域
    area = scrapy.Field()
    #小区修建年代
    year = scrapy.Field()
    #物业类型
    propertyType = scrapy.Field()
    #开发商
    developers = scrapy.Field()
    #总户数
    totalHouse = scrapy.Field()
    #小区均价
    avgPrice = scrapy.Field()
    #插入时间
    inserttime = scrapy.Field()
    
    
    