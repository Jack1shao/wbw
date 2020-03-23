
import pymysql
#from loggerClass import logger
from sqlalchemy import create_engine
class savedateClass(object):
	'''数据保存
	'''


	#私有类
	class _save_mysql(object):
		"""docstring for save_mysql"""
		def __init__(self):
			
			self.engine = create_engine("mysql+pymysql://root:123456@localhost:3306/stock?charset=utf8",encoding="utf-8", echo=True)


		def insert(self,datein,SqlInsert):
			try:
				conn=self.engine.connect()
			except Exception as e:
				print('数据库连接异常1')
				return 0
		
			try:
				cur=conn.cursor()#获取一个游标
				cur.executemany(SqlInsert,datein)
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
				conn=self.engine.connect()
			except Exception as e:
				print('数据库连接异常2')
				return 0
			try:
				dateList=[]
				cur=conn.cursor()#获取一个游标
				cur.execute(sql)
				dateList=cur.fetchall()
				conn.commit()
			except  Exception as e :
				print("发生异常",e);
				return 0
			finally:cur.close();conn.close()#释放数据库资源
			return dateList	


		def insert_by_df(self,df,tables1):
			try:
				print(self.engine)
				conn=self.engine.connect()
			except Exception as e:
				print('数据库连接异常3')
				return 0
			try:
				df.to_sql(tables1,self.engine,if_exists='append') #追加到数据库表中
			except  Exception as e :
				print("发生异常",e);
				return 0
			finally:
				conn.close()#释放数据库资源
			return 1	

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


#h=savedateClass()
#print(h.engine)
#conn=h.getconn()
#h.closeconn(conn)