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
    