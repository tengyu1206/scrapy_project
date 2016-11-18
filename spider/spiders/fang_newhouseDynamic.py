# -*- coding: utf-8 -*-

'''
  step3
  搜房网新房动态特征，根据step1中的详情页url 获取每个房源的动态特征
'''

import scrapy
from scrapy.selector import Selector
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from core.data.db.real_estate import est_house_info
from spider.items import FangNewhouseDynamicItem
import core.helpers.time_util as tu
from bs4 import BeautifulSoup
import json
import time


class Fang_newhouseDynamic_Spider(scrapy.Spider):
    custom_settings = {
        'ITEM_PIPELINES':{'spider.pipelines.FangNewhouseDynamicPipeline': 300},
    }
    name = "fang_newhouseDynamic"
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
        sql = "SELECT url,building_name,city,developer FROM est_house_info"
        result = self.table.getData(sql)
        for infos in result:
            request = scrapy.Request(infos[0],headers=self.headers,callback=self.parse)
            request.meta['newhouse_name'] = infos[1]
            request.meta['city'] = infos[2]
            request.meta['developer'] = infos[3]
            
            sql1 = "SELECT MAX(_data_version) FROM est_house_price_data WHERE url='" + infos[0] + "'"
            result1 = self.table.getData(sql1)
            data_version = 1
            if(result1[0][0] != None):
                data_version = result1[0][0] + 1                
            request.meta['data_version'] = data_version
            #print "data_version:",infos[0],data_version
            yield request
            

            #yield self.make_requests_from_url(infos[1]) 
            
    def parse(self, response):
        #print response.url
        item = FangNewhouseDynamicItem()
        
        item["newhouse_name"] = response.meta['newhouse_name']
        item["city"] = response.meta['city']
        item["developer"] = response.meta['developer']
        item["data_version"] = response.meta['data_version']
        item["url"] = response.url

        html = response.body
        soup = BeautifulSoup(html, 'html5lib')
        priceInfo = soup.select('span.prib.cn_ff')
        priceInfo_office = soup.select('span.zt22.zt_ct.ysc00')
        
        if(len(priceInfo) != 0):
            #print "type:",response.meta['type']
            price = priceInfo[0].text.strip()            
            if(price == "待定"):
                fnzoushiList = soup.select('div.fnzoushi > script')
                if(len(fnzoushiList) != 0):
                    fnzoushi = fnzoushiList[0].text.strip().split("=")[1].strip().split(";")[0]
                    json_zoushi = json.loads(fnzoushi)
                    priceGram = json_zoushi['series']
                    for pricetype in priceGram:
                        if(pricetype['datatype'] == "house"):
                            for i in pricetype['data'][::-1]:
                                if(i[1] != None):
                                    price = i[1]
                                    #print "走势价格:",i[0],i[1]
                                    break
            try:
                item['avgPrice'] = int(price)
            except:
                item['avgPrice'] = None            
            #print "价格:",item['avgPrice']                    
            open_type = soup.select("div.information")[0]
            open_type1 = open_type.find(id='xfptxq_B03_08') 
            open_type2 = open_type.find(id='xfdsxq_B04_23')
            open_type3 = open_type.find(id='xfptxq_B04_23')   
            if(open_type1 != None):
                open_time =  open_type1['title']
                item['openDate'] = open_time
                #print "开盘时间1:",item['openDate']
            elif(open_type2 != None):
                open_time = open_type2['title']
                item['openDate'] = open_time
                #print "开盘时间2:",item['openDate']
            elif(open_type3 != None):
                open_time = open_type3['title']
                item['openDate'] = open_time
                #print "开盘时间3:",item['openDate']
            else:
                item['openDate'] = None
                #print "开盘时间:","None"
            
            deliverDateList = soup.select('div.lpnametc > table > tbody > tr')
            if(len(deliverDateList) != 0):
                deliverDate = deliverDateList[2]
                item['deliverDate'] = deliverDate.td.text.strip()
                #print "交房时间:",item['deliverDate']
            else:
                item['deliverDate'] = None
                #print "交房时间:","None"
                
            status = soup.find(id="txt_sale_rate")["value"]
            item['status'] = status
            #print "status111111111111:",status
            
            rent_typetag = soup.find(id='xfxq_B03_14')
            if(rent_typetag == None):
                rent_typetag = soup.find(id='xfdsxq_B03_14')
                if(rent_typetag == None):
                    rent_typetag = soup.find(id='xfptxq_B03_14')
            
            if(rent_typetag != None):
                rent_url = rent_typetag['href']
                request = scrapy.Request(rent_url,headers=self.headers,callback=self.parse_rentprice_data)
                request.meta['item_temp'] = item
                yield request
                time.sleep(5)
        
        if(len(priceInfo_office) != 0):
            price = priceInfo_office[0].text.strip()
            try:
                item['avgPrice'] = int(price)
            except:
                item['avgPrice'] = None
            #print "office_price:",price
            
            opentimeList = soup.select("div.cd_fir_xx_b.FL")
            if(len(opentimeList) != 0):
                opentime = opentimeList[0].ul.li.text.strip().split(" ")[1]
                item['openDate'] = opentime
                #print "office_开盘时间:",opentime
            
            left_info = soup.select('div.cd_fir_xx_a.FL')[0]
            detail_url = left_info.select('ul > li')[-1].a['href']
            deliver_url = detail_url.replace('housedetail','live_history')
            
            status = left_info.select('ul > li')[0].text.strip().split(" ")[1]
            item['status'] = status
            #print "status2222222222222:",status
            #print deliver_url
            request = scrapy.Request(deliver_url,headers=self.headers,callback=self.parse_office_deliver_data)
            request.meta['item_temp'] = item
            #request.meta['type'] = response.meta['type']
            yield request
            time.sleep(6)
          
        
    
    def parse_rentprice_data(self, response):
        #print response.url
        item = response.meta['item_temp']
        
        item['rentPrice'] = None
        html = response.body
        soup = BeautifulSoup(html, 'html5lib')
        rentinfo = soup.select('div.esfHousedetail > p')
        if(len(rentinfo) != 0):
            rentprice = rentinfo[1].span.text.strip().split("元/平")[0]
            if(rentprice != ""):
                item['rentPrice'] = rentprice
        item["inserttime"] = tu.today() 
        yield item    
                           
                
    def parse_office_deliver_data(self, response):
        #print response.url
        item = response.meta['item_temp'] 
        #print "type:",response.meta['type']
        #print "价格:",item['avgPrice']
        #print "开盘时间:",item['openDate']
        
        html = response.body
        soup = BeautifulSoup(html, 'html5lib')        
        deliverDateList = soup.select('div.kpjjlu > table > tbody > tr')
        if(len(deliverDateList) > 1):
            deliverDate = deliverDateList[1]
            item['deliverDate'] = deliverDate.td.text.strip()
            #print "交房时间:",item['deliverDate']
        else:
            item['deliverDate'] = None
            #print "交房时间:","None"
        item["inserttime"] = tu.today()
        item["rentPrice"] = None
        time.sleep(5)
        yield item
        
        
                   
            
                
        
                              

        

        