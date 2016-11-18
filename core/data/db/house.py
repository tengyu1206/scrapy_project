#!/usr/bin/env python
#-*-coding:utf8-*-

import os
from core.data.db.base import Base

DBNAME = os.path.basename(__file__).split('.')[0]#当前文件对应的数据库

class rong_rates(Base): # 表名
    def __init__(self):
        super(rong_rates,self).__init__(DBNAME,self.__class__.__name__)#初始化基础类

class fang_community(Base):
    def __init__(self):
        super(fang_community,self).__init__(DBNAME,self.__class__.__name__)#初始化基础类
        
class fang_community_price(Base):
    def __init__(self):
        super(fang_community_price,self).__init__(DBNAME,self.__class__.__name__)#初始化基础类

class est_house_info(Base):
    def __init__(self):
        super(est_house_info,self).__init__(DBNAME,self.__class__.__name__)#初始化基础类    
        
class fang_newhouse_dynamic(Base):
    def __init__(self):
        super(fang_newhouse_dynamic,self).__init__(DBNAME,self.__class__.__name__)#初始化基础类    