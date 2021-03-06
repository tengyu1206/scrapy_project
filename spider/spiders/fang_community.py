# -*- coding: utf-8 -*-

'''
  搜房网小区基本信息
'''
import scrapy
from scrapy.selector import Selector
import sys
from numpy import rate
reload(sys)
sys.setdefaultencoding('utf-8')
import random
import time
import core.helpers.time_util as tu
import core.helpers.utils as util
from spider.items import FangCommunityItem
import re

class Fang_community_Spider(scrapy.Spider):
    custom_settings = {
        'ITEM_PIPELINES':{'spider.pipelines.FangCommunityPipeline': 300},
    }
    name = "fang_community"
    allowed_domains = ["fang.com"]
    start_urls = (
        'http://esf.fang.com/newsecond/esfcities.aspx',
    )

    def parse(self, response):
        condif="/housing/"
        sel = Selector(response)
        cityList = sel.xpath('//div[@class="outCont"]//a')
        for city in cityList:
            domain = city.xpath('@href').extract()[0]
            index = domain+condif
            cityName = city.xpath('text()').extract()[0]
            request = scrapy.Request(index,callback=self.parse_fang_page_data)
            request.meta['cityName'] = cityName            
            #time.sleep(random.randint(1, 10))
            time.sleep(5)
            yield request

                
            

    def parse_fang_page_data(self, response):
        sel = Selector(response)
        print response.url
        urlpattern = response.url + "__0_0_0_0_pageindex_0_0"
        print sel.xpath('//span[@class="txt"]/text()').extract()[0]
        total_page = sel.xpath('//span[@class="txt"]/text()').extract()[0][1:-1]
        pageindex = 1
        #total_page = 1  #测试使用
        while pageindex <= int(total_page):
            url=urlpattern.replace('pageindex',str(pageindex))
            pageindex = pageindex + 1
            request = scrapy.Request(url,callback=self.parse_fang_communityurl_data)
            request.meta['cityName'] = response.meta['cityName']
            #time.sleep(random.randint(1, 3)) 
            time.sleep(6)           
            yield request
        
    def parse_fang_communityurl_data(self, response):
        print response.url
        print "fengle"
        sel = Selector(response)
        communityList = sel.xpath('//a[@class="plotTit"]')
        for community in communityList:
            communityName = community.xpath('text()').extract()[0]
            communityUrl = community.xpath('@href').extract()[0]
            if "http" in communityUrl:
                request = scrapy.Request(communityUrl,callback=self.parse_fang_community_data)
                request.meta['cityName'] = response.meta['cityName']
                request.meta['communityName'] = communityName
                #time.sleep(random.randint(1, 3))  
                time.sleep(15)              
                yield request
                
                            
        
    def parse_fang_community_data(self, response):
        item = FangCommunityItem()
        
        print "城市:",response.meta['cityName']
        item["cityName"] = response.meta['cityName']
        
        
        communityName = response.meta['communityName']
        item["communityName"] = communityName
        print "小区:",communityName
        
        url = response.url
        item["communityUrl"] = url
        print "小区url:",url
        
        today = tu.todaystr()
        url = url.encode('utf-8')
        communityName = communityName.encode('utf-8')
        rid = url+communityName
        rid = util.md5(rid)
        print "rid:",rid
        item["rid"] = rid
        
        sel = Selector(response)
        aliasName = sel.xpath('//span[@class="con_max"]/text()').extract()
        if len(aliasName) != 0:
            aliasName = aliasName[0][3:]
        else:
            aliasName = None
        print "小区别名:",aliasName 
        item["aliasCommunity"] = aliasName
        
        #初始化
        item["area"] = None
        item["year"] = None
        item["totalHouse"] = None
        item["propertyType"] = None
        item["developers"] = None
        item["avgPrice"] = None
        
        
        communityInfoList = sel.xpath('//div[@class="plptinfo_list clearfix"]/ul/li')
        if len(communityInfoList) != 0 :
            for info in communityInfoList:
                infoname = info.xpath('strong/text()').extract()[0]
                infoContent = None
                if len(info.xpath('text()')) != 0:
                    infoContent = info.xpath('text()').extract()[0]               
                
                if "所在区域" in infoname:
                    print "所在区域:",infoContent
                    item["area"] = infoContent
                elif "建筑年代" in infoname:
                    print "建筑年代:",infoContent
                    item["year"] = infoContent
                elif "总 户 数" in infoname:
                    print "总户数:",infoContent[0:-1]
                    item["totalHouse"] = infoContent[0:-1]
                elif "物业类型" in infoname:
                    print "物业类型:",infoContent
                    item["propertyType"] = infoContent
                elif "开 发 商" in infoname:
                    print "开发商:",infoContent
                    item["developers"] = infoContent
        
        otherInfoList = sel.xpath('//div[@class="plptinfo_tip"]/ul/li')
        if len(otherInfoList) != 0:
            otherinfo = otherInfoList[0] 
            avgPrice = otherinfo.xpath('//strong[@class="red"]/text()').extract()[0]
            print "平均价格:",avgPrice
            item["avgPrice"] = avgPrice
                              
        item["inserttime"] = tu.datetime()    
        yield item    
        
        
        
        
            
        
        
            
        
        
            
        