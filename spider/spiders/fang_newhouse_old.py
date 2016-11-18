# -*- coding: utf-8 -*-

'''
  step1：
   搜房网获取新房信息，第一步获取基本信息以及详情页url
  基本信息:id,name,city,url,state
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
from spider.items import FangNewhouseStaticItem
import re
from bs4 import BeautifulSoup
import requests

class Fang_newhouse_Spider(scrapy.Spider):
    custom_settings = {
        'ITEM_PIPELINES':{'spider.pipelines.FangNewhouseUrlPipeline': 300},
    }
    name = "fang_newhouse_old"
    allowed_domains = ["fang.com"]
    start_urls = (
        'http://newhouse.fang.com/house/s/',
    )
    
    headers = {
      "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
      "Accept-Language":"zh-CN,zh;q=0.8",
      "Accept-Encoding":"gzip, deflate, sdch",
      "Referer":"http://www.rong360.com/cityNavi.html",
      "Cookie":"global_cookie=6noxd9kubsghuk29or6dhlrmd1oistwjlfh; passport=username=&password=&isvalid=1&validation=; _jzqx=1.1476930975.1478498063.9.jzqsr=newhouse%2Efang%2Ecom|jzqct=/house/s/b92/.jzqsr=newhouse%2Efang%2Ecom|jzqct=/house/s/; _jzqa=1.3805844646053927000.1476930975.1477964590.1478498063.14; SoufunSessionID_Esf=1_1478509222_6161; searchLabelN=1_1478740502_13287%5B%3A%7C%40%7C%3A%5D025a45300b18b1a1cb529b4443c9b3f7; searchConN=1_1478740502_13691%5B%3A%7C%40%7C%3A%5De4b70ed87e45d9b5f3b4662d27757f55; SearchKeywordHistoryTJ=%25d4%25c2%25b9%25e2%25d4%25b0%255e2016%252f11%252f1%2b9%253a20%253a23%257c%25b2%25fd%25ba%25a3%25b9%25ab%25d4%25a2%255e2016%252f11%252f11%2b15%253a02%253a11; vh_shop=1_1477901714_12589%5B%3A%7C%40%7C%3A%5D23548ef2283f0cd1216affdef712c075; showAdtj=1; newhouse_chat_guid=E70312F7-A319-25F6-61DB-CCD96A11A5EC; recentViewlpNew_newhouse=1_1478109949_4212%5B%3A%7C%40%7C%3A%5De8ca8a579aa53dc6d9c3d2d3d4b93d92; Captcha=39426F38705165436E3348636D51536E4A346A71374F43456B325536527970557237526D4678474875574C4A6A682F4C626834746E536E636D392B47306A525767414678443938643368413D; vh_newhouse=1_1473313970_10224%5B%3A%7C%40%7C%3A%5D22e0119302c5e4c23ecc76bfa110e182; jiatxShopWindow=1; newhouse_ac=1_1479106224_9512%5B%3A%7C%40%7C%3A%5Df632db8783931edac9d08e7e7e58cea2; token=; newhouse_user_guid=448DFB1C-D436-5B78-2585-D94AFBFDFD35; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; __utmt_t3=1; __utmt_t4=1; new_search_uid=2bef37ba23d18613b060be03c3cec3e5; sf_source=; s=; indexAdvLunbo=; city=tj; __utma=147393320.2038825322.1473313040.1479101367.1479105711.98; __utmb=147393320.138.10.1479105711; __utmc=147393320; __utmz=147393320.1479105711.98.56.utmcsr=newhouse.tj.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/house/dianshang/b92/; unique_cookie=U_6xzkfow36cvpygl9cgmgyntcj1hivhd97et*85",
      "Connection":"keep-alive",
      "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
    }

    #获取城市列表
    def parse(self, response):
        #print response.url
        
        '''
        #先改成beautifulsoup 试一下能不能解决close cleanly问题
        sel = Selector(response)
        cityList = sel.xpath('//div[@class="city20141104nr"]')
        '''
        
        
        #只爬取北京数据 所以先注释 所有城市的
        html = response.body
        
        #html=requests.get(response.url).content        
        soup = BeautifulSoup(html, 'html5lib')
        cityList = soup.select('div.city20141104nr')
        count = 1
        for city in cityList:
            if count > 1:            
                #cityInfoList = city.xpath('a')
                cityInfoList = city.find_all('a')                              
                for cityinfo in cityInfoList:
                    #之前的版本
                    #cityName = cityinfo.xpath('text()').extract()[0]
                    cityName = cityinfo.text.strip()
                    #之前的版本
                    #url = cityinfo.xpath('@href').extract()[0]
                    url= cityinfo['href'].strip()
                    onsellUrl = url + "b81/"
                    waitsale = url + "b82/"               
                    #print cityName,url
                    request = scrapy.Request(onsellUrl,headers=self.headers,callback=self.parse_fang_page_data)
                    request.meta['cityName'] = cityName
                    request.meta['state'] = "在售" #在售
                    yield request
                    time.sleep(7)
                    request1 = scrapy.Request(waitsale,headers=self.headers,callback=self.parse_fang_page_data)
                    request1.meta['cityName'] = cityName
                    request1.meta['state'] = "待售" #待售
                    yield request1
                    time.sleep(5)                                 
            count = count + 1
        
        '''
        #只爬取北京数据
        url = "http://newhouse.fang.com/house/s/"
        onsellUrl = url + "b81"
        waitsale = url + "b82"
        #print cityName,url
        request = scrapy.Request(onsellUrl,callback=self.parse_fang_page_data)
        request.meta['cityName'] = "北京"
        request.meta['state'] = "在售" #在售
        yield request
        request1 = scrapy.Request(waitsale,callback=self.parse_fang_page_data)
        request1.meta['cityName'] = "北京"
        request1.meta['state'] = "待售" #待售
        yield request1
        time.sleep(5) 
        ''' 
      
    #获取每个城市列表中每页的地址        
    def parse_fang_page_data(self, response):
        ''' 
        #之前的版本
        sel = Selector(response)
        lastPage = sel.xpath('//a[@class="last"]/@href')
        '''
        
        
        html = response.body
        #html=requests.get(response.url).content
        soup = BeautifulSoup(html, 'html5lib')
        lastPage = soup.select('a.last')       
        totalPage = 1
        if len(lastPage) == 1:
            #之前的版本
            #totalPage = lastPage.extract()[0].split("b9")[1][0:-1]
            totalPage = lastPage[0]['href'].strip().split("b9")[1][0:-1]            
        pageindex = 1
        while pageindex <= int(totalPage):
            url = response.url
            #print "城市列表-看url结尾有没有/:",response.url
            if url.endswith("/"):
                url = response.url[0:-1]+"-b9"+str(pageindex) + "/"
            else:
                url = url + "-b9"+str(pageindex) + "/"
            pageindex = pageindex + 1
            #print "加上页数的url:",url
            request = scrapy.Request(url,headers=self.headers,callback=self.parse_fanglist_data)
            request.meta['cityName'] = response.meta['cityName']
            request.meta['state'] = response.meta['state']
            yield request
            time.sleep(5)

    #获取每页地址中每个房源首页地址                   
    def parse_fanglist_data(self, response):
        #如果有新房自营，进入该网址爬取第一条 新parse,else 
        '''
        sel = Selector(response)
        houseList = sel.xpath('//div[@class="nl_con clearfix"]/ul/li')
        '''
        #print "有没有/:",response.url
        html = response.body
        #html=requests.get(response.url).content
        soup = BeautifulSoup(html, 'html5lib')
        houseList = soup.select('div.nl_con.clearfix > ul > li')        
        #print "list:",len(houseList)
        item = FangNewhouseStaticItem()
        for houseinfo in houseList:
            #之前的版本
            #selfsale = houseinfo.xpath('@class').extract() 
            
            #之前的版本               
            #if len(selfsale) == 1:
            if(len(houseinfo.attrs) != 0):
                #之前的版本  
                #if selfsale[0] == "fffbf2":
                if houseinfo['class'][0] == "fffbf2":
                    #之前的版本  
                    #houseBaseinfo = houseinfo.xpath('.//div[@class="nlcd_name"]/a')
                    #houseName = houseBaseinfo.xpath('text()').extract()[0].strip()
                    houseBaseinfo = houseinfo.select('div.nlcd_name > a')
                    houseName = houseBaseinfo[0].text.strip()  
                         
                    #之前的版本 
                    #houseurl = "http://newhouse.fang.com" + houseBaseinfo.xpath('@href').extract()[0].strip()
                    
                    houseurl = "http://newhouse.fang.com" + houseBaseinfo[0]['href'].strip()
                    #print "newsale_url:",houseurl
                   
                    
                    request = scrapy.Request(houseurl,headers=self.headers,callback=self.parse_selfsale_data)
                    request.meta['cityName'] = response.meta['cityName']
                    request.meta['state'] = response.meta['state']
                    request.meta['newhouse_name'] = houseName
                    yield request
                    time.sleep(4)  
                              
            else:
                #之前的版本
                #houseBaseinfo = houseinfo.xpath('.//div[@class="nlcd_name"]/a')
                #houseName = houseBaseinfo.xpath('text()').extract()[0].strip()
                
                houseBaseinfo = houseinfo.select('div.nlcd_name > a')
                houseName = houseBaseinfo[0].text.strip()
                
                #之前的版本
                #houseurl = houseBaseinfo.xpath('@href').extract()[0].strip()                
                houseurl = houseBaseinfo[0]['href'].strip()
                
                
                item["url"] = houseurl
                #print "url:",item["url"]
                item["newhouse_name"] = houseName
                #print "newhouseName:",item["newhouse_name"]
                region = houseinfo.select('div.address > a')[0].text.strip().split("[")[1].strip().split("]")[0].strip()
                if(region == ""):
                    region = None
                
                item["region"] = region
                #print "region:",region
                item["city"] = response.meta['cityName']
                #print "city:",item["city"]
                item["state"] = response.meta['state']
                #print "state:",item["state"]
                
                
                '''
                item["inserttime"] = tu.datetime()
                
                url = houseurl.encode('utf-8')
                houseName = houseName.encode('utf-8')
                rid = url+houseName
                rid = util.md5(rid)
                print "rid:",rid
                item["newhouse_id"] = rid
                '''
                yield item
                time.sleep(5)
                      
                
        '''
                #这些先不要，因为改存数据库了，不继续向下走
                request = scrapy.Request(houseurl,callback=self.parse_ordinary_data)
                request.meta['cityName'] = response.meta['cityName']
                request.meta['state'] = response.meta['state']
                request.meta['newhouse_name'] = houseName
                yield request
                time.sleep(5)
                '''
    '''
    #这些先不要，先不继续往下取
    def parse_ordinary_data(self, response): 
        print response.url
        #初始化
        item = FangNewhouseStaticItem()
        item["newhouse_id"] = None
        #item["newhouse_name"] = None
        #item["city"] = None   
        #item["url"] =  None
        #楼盘地址
        item["houseAddress"] = None
        #开发商
        item["developers"] = None
        #状态 在售还是待售
        #item["state"] = None
        item["inserttime"] = None
        
        item["city"] = response.meta['cityName']
        print "city:",item["city"]
        item["state"] = response.meta['state']
        print "state:",item["state"]
        item["newhouse_name"] = response.meta['newhouse_name']
        print "newhouseName:",item["newhouse_name"]
        item["url"] = response.url
        print "url:",item["url"]
        
        url = response.url.encode('utf-8')
        houseName = response.meta['newhouse_name'].encode('utf-8')
        rid = url+houseName
        rid = util.md5(rid)
        print "rid:",rid
        item["newhouse_id"] = rid
        
        sel = Selector(response)
        detailInfoList = sel.xpath('//div[@class="fl more"]/p/a/@href').extract()
        if len(detailInfoList) != 0:
            detailInfoUrl = detailInfoList[0].strip()
            print "详细url:",detailInfoUrl
        else:
            print "该url有问题:",url
 '''       
                
        
                   
    def parse_selfsale_data(self, response):  
        #print "新房自营列表页:",response.url
        #以前的版本
        #sel = Selector(response)
        #houseList = sel.xpath('//div[@class="nl_con clearfix"]/ul/li')  
        #firstSelfsaleUrl = houseList[0].xpath('.//div[@class="nlcd_name"]/a/@href').extract()[0].strip()
        
        html = response.body
        #html=requests.get(response.url).content
        soup = BeautifulSoup(html, 'html5lib')
        houseList = soup.select('div.nl_con.clearfix > ul > li')
        firstSelfsaleUrl = houseList[0].select('div.nlcd_name > a')[0]['href']        
        #print "fistself_url:",firstSelfsaleUrl
        region = houseList[0].select('div.address > a')[0].text.strip().split("[")[1].strip().split("]")[0].strip()
        if(region == ""):
            region = None
        
        
        item = FangNewhouseStaticItem()
        
        item["newhouse_name"] = response.meta['newhouse_name']
        #print "newhouseName:",item["newhouse_name"]
        item["url"] = firstSelfsaleUrl
        #print "url:",item["url"]
        item["region"] = region
        #print "region:",region
        item["city"] = response.meta['cityName']
        #print "city:",item["city"]
        item["state"] = response.meta['state']
        #print "state:",item["state"]
        
        '''
        item["inserttime"] = tu.datetime() 

        url = firstSelfsaleUrl.encode('utf-8')
        houseName = response.meta['newhouse_name'].encode('utf-8')
        rid = url+houseName
        rid = util.md5(rid)
        print "rid:",rid
        item["newhouse_id"] = rid
        '''
        yield item
        time.sleep(5)
        
        
        
        
        '''
        #下面先不用 
        request = scrapy.Request(firstSelfsaleUrl,callback=self.parse_ordinary_data)
        request.meta['cityName'] = response.meta['cityName']
        request.meta['state'] = response.meta['state']
        request.meta['newhouse_name'] = response.meta['newhouse_name']
        yield request
        time.sleep(4)  
        '''
        
        
        
            
        
        
            
        
        
            
        