#!/usr/bin/env python
#-*-coding:utf8-*-
"""
关于行业数据的存储地址
"""
from core.helpers.mysql import Connection

class Base(object):
    """石油期货的数据，包括WTI和布兰特石油
    """
    def __init__(self,dbName,tableName):
        self._cnn = Connection(dbName)#建立连接
        self._tableName = tableName#获取操作的表名

    def getData(self,sql=None):
        """获取所有的数据,用户可以输入sql语句
        """
        cnn = self._cnn
        if sql == None:
            sql = """SELECT * FROM %s"""%(self._tableName)
        #result = cnn.select(sql,kind='pandas')#获取pandas格式的数据
        result = cnn.select(sql)
        return result

    def insertData(self,data,if_exists='append',chunksize=None):
        """往表中插入数据
        """
        cnn = self._cnn
        cnn.insert(data,table=self._tableName,kind='pandas',if_exists=if_exists,chunksize=chunksize)#将历史数据插入到数据库中
    
    def updateData(self,data,sql,chunksize=None):
        cnn = self._cnn
        cnn.update(data, sql, table=self._tableName, chunksize=chunksize)
