# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from core.data.db.house import rong_rates
from core.data.db.house import fang_community
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
        dataNumPy = np.asarray([(item["rid"],item["cityName"],item["communityName"],item["communityUrl"],item["aliasCommunity"],item["area"],item["year"],item["propertyType"],item["developers"],item["totalHouse"],item["avgPrice"],item["inserttime"])])
        df = pd.DataFrame(dataNumPy,columns=['id','city','community','community_url','community_alias','area','year','property_type','developers','total_house','avg_price','inserttime'])
        #print df
        return df