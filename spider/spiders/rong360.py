# -*- coding: utf-8 -*-

'''
  融360网页爬取解析,爬取融360所有城市地址,
  根据城市URL抓去各城市各银行的贷款利率
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
from spider.items import Rong360Item
import re

class Rong360Spider(scrapy.Spider):
    custom_settings = {
        'ITEM_PIPELINES':{'spider.pipelines.RongRatesPipeline': 300},
    }
    name = "rong360"
    allowed_domains = ["rong360.com"]
    start_urls = (
        'http://www.rong360.com/cityNavi.html',
    )

    def parse(self, response):
        href = "http://www.rong360.com/"
        condif="/fangdai/search?px=1"
        sel = Selector(response)
        cityList = sel.xpath('//div[@class="city-list"]//a')
        for city in cityList:
            domain = city.xpath('@domain').extract()[0]
            cityName = city.xpath('span/text()').extract()[0]
            index = href+domain+condif
            request = scrapy.Request(index,callback=self.parse_rong360_data)
            request.meta['domain'] = domain
            request.meta['cityName'] = cityName
            time.sleep(random.randint(1, 3))
            yield request

    def parse_rong360_data(self, response):
        item = Rong360Item()
        sel = Selector(response)
        #productList = sel.xpath('//ul[@id="product_list"]')
        print response.url
        productList = sel.xpath('//div[@class="product_info fl"]')
        if len(productList) != 0:
            #print response.url,response.meta['domain'],response.meta['cityName']
            for product in productList:
                title = product.xpath('h4/a/@title').extract()[0]
                title = title.split('-')[0].strip().encode('utf-8')
                #银行名称
                item["title"] = title

                #支持类型：新房二手房()
                support_type = product.xpath('p/span[@class="house_suppot_types"]/text()').extract()[0]
                #item["support_type"] = support_type.encode('utf-8')

                house_type = product.xpath('p/span[@class="house_type"]/text()').extract()[0].replace(u'\xa0', u' ')
                hs = re.findall(r"\d*[0-9]+\d*",house_type.encode('utf-8'))
                #审批时间
                examine_time = hs[0].encode('utf-8')
                item["examine_time"] = examine_time

                #放款时间
                loan_time = hs[1].encode('utf-8')
                item["loan_time"] = loan_time

                url = response.url.encode('utf-8')
                today = tu.todaystr()
                rid = url+title+today
                rid = util.md5(rid)
                #随机id
                item["rid"] = rid

                #url
                item["url"] = url

                cityName = response.meta['cityName']
                #城市中文名称
                item["cityName"] = cityName

                item["type1_discount"] = 0.00
                item["type1_rate"] = 0.00
                item["type1_firstpay"] = 0
                item["type2_discount"] = 0.00
                item["type2_rate"] = 0.00
                item["type2_firstpay"] = 0
                item["type3_discount"] = 0.00
                item["type3_rate"] = 0.00
                item["type3_firstpay"] = 0


                featureList = product.xpath('ul[@class="features"]/li')
                if(len(featureList) != 0):
                    for feature in featureList:
                        mark = feature.xpath('i/@class').extract()[0]
                        types = feature.xpath('span[@class="type"]/text()').extract()[0]
                        rate = feature.xpath('b/text()').extract()[0]
                        #print "rate_info:",rate
                        re.findall(r"\d*[0-9]+\d*",rate.encode('utf-8'))
                        r = rate.split('(')
                        discount = re.findall(r"[-+]?[0-9]*\.?[0-9]+",r[0])
                        if (discount==[]):
                            discount = 1
                        else:
                            discount = float(discount[0])
                            if(discount>10):
                                discount = discount/100
                            elif(discount>2 and discount<10):
                                discount = discount/10
                        rate = float(re.findall(r'(\d+\.\d+)?%',r[1])[0])#提取百分数
                        first_pay = feature.xpath('span[@class="first_pay"]/text()').extract()[0]
                        fp = int(filter(str.isdigit, first_pay.encode('utf-8')))# fp 付款比例

                        if(mark == "house_type1"):
                            item["type1_discount"] = discount
                            item["type1_rate"] = rate
                            item["type1_firstpay"] = fp
                        elif(mark == "house_type2"):
                            item["type2_discount"] = discount
                            item["type2_rate"] = rate
                            item["type2_firstpay"] = fp
                        elif(mark == "house_type3"):
                            item["type3_discount"] = discount
                            item["type3_rate"] = rate
                            item["type3_firstpay"] = fp

                item["inserttime"] = tu.datetime()
                yield item
