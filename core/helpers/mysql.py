#!/usr/bin/env python
#-*-coding:utf8-*-
'''
关于Mysql的一些列使用方法
'''
import MySQLdb
import pandas as pd
from core.config import dbConfig 
#当你将一个包作为模块导入,实际上导入了它的 __init__.py 文件
#如果 __init__.py 不存在，这个目录就仅仅是一个目录，而不是一个包，它就不能被导入或者包含其它的模块和嵌套包。

class Connection(object):
	def __init__(self,datebase):
		option = dbConfig()[datebase]#获取连接的配置
		host = option['host']
		user = option['user']
		passwd = option['passwd']
		db = option['db']
		self.conn=MySQLdb.connect(host=host,user=user,passwd=passwd,db=db,charset="utf8")
	#插入多个数据
	def insert(self,data,sql=None,table=None,kind=None,if_exists='append',flavor='mysql',chunksize=None):
		conn = self.conn
		try:
			if kind == 'pandas' and table:
				data.to_sql(con=conn,name=table,index=False,if_exists=if_exists,flavor=flavor,chunksize=chunksize)#将pandas格式的数据插入到数据库中
				print '数据插入成功'
			else:
				cur=conn.cursor()
				cur.executemany(sql,data)
				conn.commit()
				cur.close()
				conn.close()
				print "数据插入成功"
		except MySQLdb.Error,e:
			print "Mysql Error %d: %s" % (e.args[0], e.args[1])
	#查询数据
	def select(self,sql,kind=None,index=None):
		conn = self.conn
		try:
			if kind == 'pandas':
				df = pd.read_sql(sql,conn,index_col=index)
				return df#返回pandas格式的数据
			else:
				cur = conn.cursor()
				cur.execute(sql)#执行SQL语句
				results = cur.fetchall()#获取所有记录的列表
				return results
		except MySQLdb.Error,e:
			print "Mysql Error %d: %s" % (e.args[0], e.args[1])
