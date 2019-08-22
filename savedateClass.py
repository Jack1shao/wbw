

import pymysql
from loggerClass import logger

class savedateClass(object):
	'''数据保存
	'''



	#私有类
	class _save_mysql(object):
		"""docstring for save_mysql"""

		def insert(self,datein,SqlInsert):
			try:
				conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='mysql',port=3306,charset='utf8')

			except Exception as e:
				print('数据库连接异常')
				#conn.close()
				return 0
			
			try:
				#conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='mysql',port=3306,charset='utf8')
				#print(conn)
				cur=conn.cursor()#获取一个游标

				cur.executemany(SqlInsert,datein)
				#print(dateIn)
				print('插入成功');
				conn.commit()
			
				
			except  Exception as e :
				print("insert 发生异常",e);

				return 0
			finally:cur.close();conn.close()#释放数据库资源
			return 1

		def select(self,sql):
			dateList=[]
			#获取一个数据库连接
			try:
				conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='mysql',port=3306,charset='utf8')

			except Exception as e:
				print('数据库连接异常')
				#conn.close()
				return 0
			try:
				dateList=[]
				#conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='mysql',port=3306,charset='utf8')
				#print(conn)
				cur=conn.cursor()#获取一个游标
				cur.execute(sql)
				dateList=cur.fetchall()
				conn.commit()
				
			except  Exception as e :
				print("发生异常",e);
				return 0
			finally:cur.close();conn.close()#释放数据库资源
			return dateList	



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


"""h=savedateClass()
conn=h.getconn()
h.closeconn(conn)"""