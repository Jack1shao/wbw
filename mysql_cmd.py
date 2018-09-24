'''
db cmd class 
sjk
20180922
		

'''

import pymysql


class mysql_cmd1(object):
	"""docstring for mysql_cmd"""
	def __init__(self, arg):
		super(mysql_cmd, self).__init__()
		self.arg = arg


	def insertMysql(dateIn,SqlInsert):

		try:
			conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='mysql',port=3306,charset='utf8')
			cur=conn.cursor()#获取一个游标
			
			cur.executemany(SqlInsert,dateIn)
			#print(dateIn)
			print('插入成功');
			conn.commit()
			cur.close()#关闭游标
			conn.close()#释放数据库资源
		except  Exception as e :print("insert 发生异常",e);return 0
		return 1

	def selectMysql(sql):
		dateList=[]
		#获取一个数据库连接
		try:
			dateList=[]
			conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='mysql',port=3306,charset='utf8')
			cur=conn.cursor()#获取一个游标
			cur.execute(sql)
			dateList=cur.fetchall()
			conn.commit()
			cur.close()#关闭游标
			conn.close()#释放数据库资源
		except  Exception as e :print("发生异常",e);return 0
		return dateList