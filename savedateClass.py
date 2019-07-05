

import pymysql
from loggerClass import logger

class savedateClass(object):
	'''数据保存
	'''



	#私有类
	class _save_mysql(object):
		"""docstring for save_mysql"""
	

		def getconn(self):
			try:
				conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='mysql',port=3306,charset='utf8')
				cur=conn.cursor()#获取一个游标
				print(cur)
			except Exception as e:
				#print("")
				logger().error("date connect error")
				cur.close();
				conn.close()
			return conn,cur,0

		def closeconn(self,conn):
			conn.close()
			return 0

		def insert(self,datein,sql):
			
				pass

		def select(self,sql):
				pass	



	instance=None
	def __new__(cls):
			if not savedateClass.instance:
				savedateClass.instance=savedateClass._save_mysql()

			return savedateClass.instance

	def __getattr__(self,name):
			return getattr(self.instance,name)

	def __setattr__(self,name):
			return setattr(self.instance,name)	
	def function():
		pass


h=savedateClass()
h.getconn()