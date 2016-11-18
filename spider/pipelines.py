# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from core.data.db.house import rong_rates
from core.data.db.house import fang_community
from core.data.db.house import fang_community_price
from core.data.db.real_estate import est_house_info
from core.data.db.real_estate import est_house_price_data
import pandas as pd
import numpy as np

class RongRatesPipeline(object):
    def __init__(self):
        self.table = rong_rates()
        
    def process_item(self, item, spider):
        data = self._changeItem(item)
        self.table.insertData(data,if_exists='append')
        return item

    def _changeItem(self,item):
        """将item数据转换成pandas格式的数据
        """
        dataNumPy = np.asarray([(item["rid"],item["cityName"],item["url"],item["title"],item["examine_time"],item["loan_time"],item["type1_discount"],item["type1_rate"],item["type1_firstpay"],item["type2_discount"],item["type2_rate"],item["type2_firstpay"],item["type3_discount"],item["type3_rate"],item["type3_firstpay"],item["inserttime"])])
        df = pd.DataFrame(dataNumPy,columns=['id','city','href','bank','approve_days','loan_day','first_discount','first_rates','first_ratio','second_discount','second_rates','second_ratio','commerical_discount','commerical_rates','commerical_ratio','update_time'])
        #print df
        return df
    
class FangCommunityPipeline(object):
    def __init__(self):
        self.table = fang_community()
        
    def process_item(self, item, spider):
        data = self._changeItem(item)
        self.table.insertData(data,if_exists='append')
        return item
    def _changeItem(self,item):
        """将item数据转换成pandas格式的数据
        """
        dataNumPy = np.asarray([(item["rid"],item["cityName"],item["communityName"],item["communityUrl"],item["aliasCommunity"],item["area"],item["year"],item["propertyType"],item["developers"],item["totalHouse"],item["inserttime"])])
        df = pd.DataFrame(dataNumPy,columns=['community_id','city','community','community_url','community_alias','area','year','property_type','developers','total_house','inserttime'])
        #print df
        return df
    
class FangCommunityPricePipeline(object):
    def __init__(self):
        self.table = fang_community_price()
        
    def process_item(self, item, spider):
        data = self._changeItem(item)
        self.table.insertData(data,if_exists='append')
        return item
    def _changeItem(self,item):
        """将item数据转换成pandas格式的数据
        """
        dataNumPy = np.asarray([(item["community_id"],item["avgPrice"],item["inserttime"])])
        df = pd.DataFrame(dataNumPy,columns=['community_id','price','inserttime'])
        #print df
        return df
    
class FangNewhouseUrlPipeline(object):
    def __init__(self):
        self.table = est_house_info()
        
    def process_item(self, item, spider):
        data = self._changeItem(item)
        self.table.insertData(data,if_exists='append')
        return item
    def _changeItem(self,item):
        """将item数据转换成pandas格式的数据
        """
        dataNumPy = np.asarray([(item["city"],item["newhouse_name"],item["url"],item["region"])])
        df = pd.DataFrame(dataNumPy,columns=['city','building_name','url','region'])
        #print df
        return df

class FangNewhouseDetailPipeline(object):
    def __init__(self):
        self.table = est_house_info()
        
    def process_item(self, item, spider):
        data = self._changeItem(item)
        sql = "update " + self.table._tableName + " set building_type=%s,address=%s,developer=%s,rights_year=%s,decoration_condition=%s,building_area=%s,cover_area=%s,plot_ratio=%s,green_rate=%s,building_num=%s,house_num=%s,property_charges=%s,property_company=%s,floor_desc=%s,_data_version=%s where url=%s"
        self.table.updateData(data,sql)
        return item
    def _changeItem(self,item):
        """将item数据转换成pandas格式的数据
        """
        tupledata = (item["type"],item["houseAddress"],item["developers"],item["year"],item["decoration"],item["structure_area"],item["floor_area"],item["plot_ratio"],item["green_rate"],item["building_num"],item["household_num"],item["property_fee"],item["property_company"],item["floor"],item["data_version"],item["url"])
        #dataNumPy = np.asarray([(item["type"],item["houseAddress"],item["developers"],item["year"],item["decoration"],item["structure_area"],item["floor_area"],item["plot_ratio"],item["green_rate"],item["building_num"],item["household_num"],item["property_fee"],item["property_company"],item["floor"],item["newhouse_id"])])
        #df = pd.DataFrame(dataNumPy,columns=['type','houseaddress','developer','year','decoration','structure_area','floor_area','plot_ratio','green_rate','building_num','household_num','property_fee','property_company','floor','newhouse_id'])
        return tupledata
    
class FangNewhouseDynamicPipeline(object):
    def __init__(self):
        self.table = est_house_price_data()
        
    def process_item(self, item, spider):
        data = self._changeItem(item)
        self.table.insertData(data,if_exists='append')
        return item
    def _changeItem(self,item):
        """将item数据转换成pandas格式的数据
        """
        dataNumPy = np.asarray([(item["inserttime"],item["newhouse_name"],item["avgPrice"],item["openDate"],item["deliverDate"],item["rentPrice"],item["developer"],item["city"],item["data_version"],item["status"],item["url"])])
        df = pd.DataFrame(dataNumPy,columns=['report_date','building_name','refer_price','open_date','handing_date','rent_price','developer','city','_data_version','status','url'])
        #print df
        return df
    
    
    