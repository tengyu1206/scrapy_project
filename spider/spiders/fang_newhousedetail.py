# -*- coding: utf-8 -*-

'''
  step2：
   搜房网获取新房信息:其他静态特征 ，
   根据step1中存入数据库中的详情页url获取每一个房源的静态特征
'''

import scrapy
from scrapy.selector import Selector
import sys
from pip._vendor.requests.models import Response
reload(sys)
sys.setdefaultencoding('utf-8')
from core.data.db.real_estate import est_house_info
from spider.items import FangNewhouseItem
import core.helpers.time_util as tu
from bs4 import BeautifulSoup
import random
import time


class Fang_newhouseDetail_Spider(scrapy.Spider):
    custom_settings = {
        'ITEM_PIPELINES':{'spider.pipelines.FangNewhouseDetailPipeline': 300},
    }
    name = "fang_communityDetail"
    allowed_domains = ["fang.com"]
    
    headers = {
      "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
      "Accept-Language":"zh-CN,zh;q=0.8",
      "Accept-Encoding":"gzip, deflate, sdch",
      "Cookie":"global_cookie=6noxd9kubsghuk29or6dhlrmd1oistwjlfh; passport=username=&password=&isvalid=1&validation=; _jzqx=1.1476930975.1478498063.9.jzqsr=newhouse%2Efang%2Ecom|jzqct=/house/s/b92/.jzqsr=newhouse%2Efang%2Ecom|jzqct=/house/s/; _jzqa=1.3805844646053927000.1476930975.1477964590.1478498063.14; SoufunSessionID_Esf=1_1478509222_6161; searchLabelN=1_1478740502_13287%5B%3A%7C%40%7C%3A%5D025a45300b18b1a1cb529b4443c9b3f7; searchConN=1_1478740502_13691%5B%3A%7C%40%7C%3A%5De4b70ed87e45d9b5f3b4662d27757f55; SearchKeywordHistoryTJ=%25d4%25c2%25b9%25e2%25d4%25b0%255e2016%252f11%252f1%2b9%253a20%253a23%257c%25b2%25fd%25ba%25a3%25b9%25ab%25d4%25a2%255e2016%252f11%252f11%2b15%253a02%253a11; vh_shop=1_1477901714_12589%5B%3A%7C%40%7C%3A%5D23548ef2283f0cd1216affdef712c075; showAdtj=1; newhouse_chat_guid=E70312F7-A319-25F6-61DB-CCD96A11A5EC; recentViewlpNew_newhouse=1_1478109949_4212%5B%3A%7C%40%7C%3A%5De8ca8a579aa53dc6d9c3d2d3d4b93d92; Captcha=39426F38705165436E3348636D51536E4A346A71374F43456B325536527970557237526D4678474875574C4A6A682F4C626834746E536E636D392B47306A525767414678443938643368413D; vh_newhouse=1_1473313970_10224%5B%3A%7C%40%7C%3A%5D22e0119302c5e4c23ecc76bfa110e182; jiatxShopWindow=1; newhouse_ac=1_1479106224_9512%5B%3A%7C%40%7C%3A%5Df632db8783931edac9d08e7e7e58cea2; token=; newhouse_user_guid=448DFB1C-D436-5B78-2585-D94AFBFDFD35; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; __utmt_t3=1; __utmt_t4=1; new_search_uid=2bef37ba23d18613b060be03c3cec3e5; sf_source=; s=; indexAdvLunbo=; city=tj; __utma=147393320.2038825322.1473313040.1479101367.1479105711.98; __utmb=147393320.138.10.1479105711; __utmc=147393320; __utmz=147393320.1479105711.98.56.utmcsr=newhouse.tj.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/house/dianshang/b92/; unique_cookie=U_6xzkfow36cvpygl9cgmgyntcj1hivhd97et*85",
      "Connection":"keep-alive",
      "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
    }

    
    def start_requests(self):
        self.table = est_house_info()
        sql = "SELECT url,_data_version FROM est_house_info"
        sql1 = "SELECT MAX(_data_version) FROM est_house_info"
        
        result1 = self.table.getData(sql1)
        data_version = result1[0][0] + 1
                
        result = self.table.getData(sql)
        for infos in result:
            if(infos[1] == 0):
                request = scrapy.Request(infos[0],headers=self.headers,callback=self.parse)
                request.meta['data_version'] = data_version
                yield request
            #yield self.make_requests_from_url(infos[1]) 
            
    def parse(self, response):
        #print response.url
        html = response.body
        soup = BeautifulSoup(html, 'html5lib')
        #普通住宅
        ordinary_typetag = soup.find(id='xfxq_B03_08')
        #写字楼 
        office_typetag = soup.find(id='officexq_B02_06')
        #商铺
        shop_typetag = soup.find(id='shopxq_B02_06')
        #其他
        other_typetag1 = soup.find(id='xfptxq_B03_08')
        other_typetag2 = soup.find(id='xfdsxq_B03_08')
        other_typetag3 = soup.find(id='xfzxxqy_B04_14')
        
        
            
        if(ordinary_typetag != None):
            ordinary_detailurl = ordinary_typetag['href']
            request = scrapy.Request(ordinary_detailurl,headers=self.headers,callback=self.parse_ordinary_detail_data)
            request.meta['data_version'] = response.meta['data_version']
            request.meta['url'] = response.url
            yield request
        elif(office_typetag != None):
            office_detailurl = office_typetag['href']
            request1 = scrapy.Request(office_detailurl,headers=self.headers,callback=self.parse_office_detail_data)
            request1.meta['data_version'] = response.meta['data_version']
            request1.meta['url'] = response.url
            #开发商  从首页获取
            developerInfo = soup.find(id='officexq_B03_05').select('a')
            if(len(developerInfo) != 0):
                developer = developerInfo[0].text.strip()
                request1.meta['developers'] = developer
            else:
                request1.meta['developers'] = None 
            #物业地址 从首页获取    
            propertyInfo = soup.find(id='officexq_B03_04').select('a')
            if(len(propertyInfo) != 0):
                propertyAddrs = propertyInfo[0].text.strip()
                request1.meta['property_company'] = propertyAddrs
            else:
                request1.meta['property_company'] = None 
                          
            yield request1  
            time.sleep(random.randint(1, 7))          
        elif(shop_typetag != None):
            shop_detailurl = shop_typetag['href']
            request2 = scrapy.Request(shop_detailurl,headers=self.headers,callback=self.parse_office_detail_data)
            request2.meta['data_version'] = response.meta['data_version']
            request2.meta['url'] = response.url
            #开发商  从首页获取
            developerInfo = soup.find(id='shopxq_B03_05').select('a')
            if(len(developerInfo) != 0):
                developer = developerInfo[0].text.strip()
                request2.meta['developers'] = developer
            else:
                request2.meta['developers'] = None 
            #物业地址 从首页获取    
            propertyInfo = soup.find(id='shopxq_B03_04').select('a')
            if(len(propertyInfo) != 0):
                propertyAddrs = propertyInfo[0].text.strip()
                request2.meta['property_company'] = propertyAddrs
            else:
                request2.meta['property_company'] = None
            
            yield request2 
            time.sleep(random.randint(1, 6))                       
        elif(other_typetag1 != None):
            othertype1_detailurl = other_typetag1['href']
            request3 = scrapy.Request(othertype1_detailurl,headers=self.headers,callback=self.parse_ordinary_detail_data)
            request3.meta['data_version'] = response.meta['data_version']
            request3.meta['url'] = response.url
            yield request3
            time.sleep(random.randint(1, 4))
        elif(other_typetag2 != None):
            othertype2_detailurl = other_typetag2['href']
            request4 = scrapy.Request(othertype2_detailurl,headers=self.headers,callback=self.parse_ordinary_detail_data)
            request4.meta['data_version'] = response.meta['data_version']
            request4.meta['url'] = response.url
            yield request4
            time.sleep(random.randint(1, 5))
        elif(other_typetag3 != None):
            
            othertype3_detailurl = other_typetag3['href']
            #print "ok:",othertype3_detailurl
            request5 = scrapy.Request(othertype3_detailurl,headers=self.headers,callback=self.parse_ordinary_detail_data)
            request5.meta['data_version'] = response.meta['data_version']
            request5.meta['url'] = response.url
            yield request5
            time.sleep(random.randint(1, 5))
        else:
            print "详情页不同类型的:",response.url
            

    def parse_ordinary_detail_data(self,response):
        print response.url
        item = FangNewhouseItem()
        item['data_version'] = response.meta['data_version']
        item['url'] = response.meta['url']
        html = response.body
        soup = BeautifulSoup(html, 'html5lib')
        baseinfos = soup.select('ul.list.clearfix > li')
        for infos in baseinfos:
            divs = infos.select('div')
            if("物业类别" in divs[0].text):
                item['type'] = divs[1].text.strip()
            elif("楼盘地址" in divs[0].text):
                item['houseAddress'] = divs[1].text.strip()
            elif("开发 商" in divs[0].text):
                item['developers'] = divs[1].text.strip()
            elif("产权年限" in divs[0].text):
                try:
                    item['year'] = int(divs[1].text.strip().split("年")[0])
                except:
                    item['year'] = None
            elif("装修状况" in divs[0].text):
                item['decoration'] = divs[1].text.strip().split("[")[0].strip()
            elif("建筑面积" in divs[0].text):
                try:
                    item['structure_area'] = int(divs[1].text.strip().split("平方米")[0])
                except:
                    item['structure_area'] = None
            elif("占地面积" in divs[0].text):
                try:
                    item['floor_area'] = int(divs[1].text.strip().split("平方米")[0])
                except:
                    item['floor_area'] = None
            elif("容积率" in divs[0].text):
                try:
                    item['plot_ratio'] = float(divs[1].text.strip())
                except:
                    item['plot_ratio'] = None
            elif("绿化率" in divs[0].text):
                try:
                    item['green_rate'] = float(divs[1].text.strip().split("%")[0])
                except:
                    item['green_rate'] = None
            elif("楼栋总数" in divs[0].text):
                try:
                    item['building_num'] = int(divs[1].text.strip().split("栋")[0])
                except:
                    item['building_num'] = None
            elif("总户数" in divs[0].text):
                try:
                    item['household_num'] = int(divs[1].text.strip().split("户")[0])
                except:
                    item['household_num'] = None
            elif("物业费" in divs[0].text):
                try:
                    item['property_fee'] = float(divs[1].text.strip().split("元/平方米·月")[0])
                except:
                    item['property_fee'] = None
            elif("物业公司" in divs[0].text):
                item['property_company'] = divs[1].text.strip()
            elif("楼层状况" in divs[0].text):
                item['floor'] = divs[1].text.strip()
        yield item
        time.sleep(5)
                
    def parse_office_detail_data(self,response):
        print response.url 
        item = FangNewhouseItem()
        item['data_version'] = response.meta['data_version']
        item['url'] = response.meta['url']
        item['household_num'] = None
        item['developers'] = response.meta['developers']
        item['property_company'] = response.meta['property_company']
        html = response.body
        soup = BeautifulSoup(html, 'html5lib')
        baseinfos = soup.select('div.besic_inform > table > tbody > tr > td') 
        for infos in baseinfos:
            info = infos.text.strip().split(' ')
            if(info[0] == "写字楼类型" or info[0] == "商铺类型"):
                item['type'] = info[1].strip()
            elif(info[0] == "物业地址"):
                item['houseAddress'] = info[1].strip()
            elif(info[0] == "产权年限"):
                try:
                    item['year'] = int(info[1].strip().split("年")[0])
                except:
                    item['year'] = None
            elif(info[0] == "装修状况"):
                item['decoration'] = info[1].strip().split('[')[0].strip()
            elif(info[0] == "建筑面积"):
                try:
                    item['structure_area'] = float(info[1].strip().split("平方米")[0])
                except:
                    item['structure_area'] = None
            elif(info[0] == "占地面积"):
                try:
                    item['floor_area'] = float(info[1].strip().split("平方米")[0])
                except:
                    item['floor_area'] = None
            elif(info[0] == "容 积 率"):
                plot_ratio = info[1].strip().split('[')[0].strip()
                try:
                    plot_ratio = float(plot_ratio)
                except:
                    plot_ratio = None
                item['plot_ratio'] = plot_ratio
            elif(info[0] == "绿 化 率"):                
                green_rate = info[1].strip().split('[')[0].strip()
                try:
                    green_rate = float(green_rate.split("%")[0])
                except:
                    green_rate = None
                item['green_rate'] = green_rate
            elif(info[0] == "当期楼栋数" or info[0] == "商铺总套数"):
                try:
                    item['building_num'] = int(info[1].strip().split("栋")[0])
                except:
                    item['building_num'] = None
            elif(info[0] == "物业管理费"):
                try:
                    item['property_fee'] = float(info[1].strip().split("元/平方米·月")[0])
                except:
                    item['property_fee'] = None
                
        otherinfos = soup.select('div.lineheight')
        basestr = otherinfos[-4].text.replace("\r\n","").replace(' ','').strip()
        if(otherinfos[-4].text.replace("\r\n","").replace(' ','').strip() == ""):
            item['floor'] = None
        elif("楼层状况" in basestr):
            item['floor'] = basestr.split("楼层状况：")[1].split("标准层高：")[0].strip()
        else:
            item['floor'] = None
                
        yield item
        time.sleep(7)        
            

        
                  
                
                
                
                
                
                
                
                
 
            
            
            
        
        
        
        

                              

        

        