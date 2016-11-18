# -*- coding: utf-8 -*-

'''
  搜房网小区动态信息，价格
'''

import scrapy
from scrapy.selector import Selector
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from core.data.db.house import fang_community
from spider.items import FangCommunityPriceItem
import core.helpers.time_util as tu


class Fang_communityPrice_Spider(scrapy.Spider):
    custom_settings = {
        'ITEM_PIPELINES':{'spider.pipelines.FangCommunityPricePipeline': 300},
    }
    name = "fang_communityPrice"
    allowed_domains = ["fang.com"]

    
    def start_requests(self):
        self.table = fang_community()
        sql = "SELECT community_id,community_url FROM fang_community"
        result = self.table.getData(sql)
        for infos in result:
            request = scrapy.Request(infos[1],callback=self.parse)
            request.meta['community_id'] = infos[0]
            yield request

            #yield self.make_requests_from_url(infos[1]) 
            
    def parse(self, response):
        item = FangCommunityPriceItem()
        sel = Selector(response)
        
        item["community_id"] = response.meta['community_id']
        item["avgPrice"] = None
        item["inserttime"] = tu.datetime() 
                
        otherInfoList = sel.xpath('//div[@class="plptinfo_tip"]/ul/li')
        if len(otherInfoList) != 0:
            otherinfo = otherInfoList[0] 
            avgPrice = otherinfo.xpath('//strong[@class="red"]/text()').extract()[0]
            #print "平均价格:",avgPrice
            item["avgPrice"] = avgPrice
        yield item 
                              

        

        