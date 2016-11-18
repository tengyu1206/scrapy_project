#-*-coding:utf8-*-

import os
from core.data.db.base import Base

DBNAME = os.path.basename(__file__).split('.')[0]#当前文件对应的数据库

class est_house_info(Base):
    def __init__(self):
        super(est_house_info,self).__init__(DBNAME,self.__class__.__name__)#初始化基础类    
        
class est_house_price_data(Base):
    def __init__(self):
        super(est_house_price_data,self).__init__(DBNAME,self.__class__.__name__)#初始化基础类    
