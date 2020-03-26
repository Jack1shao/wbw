#gu_save
import tushare as ts
import datetime
import os
from pandas import read_csv
from pandas.core.frame import DataFrame
class gu_save(object):
	"""docstring for gu_save"""
	def __init__(self, arg):
		super(gu_save, self).__init__()
		self.arg = arg
		

	def get_csvmc(self,code):
		csv_path='d:/stock_csv/{}.csv'.format(code)
		return csv_path

	#从接口取数
	def get_k_from_api(self,code,ktype1):
		k_li=['m','w','D','30']
		if ktype1 not in k_li:
			print("k线类型错误")
			return 0
		if len(code)!=6:
			print("股票代码不是6位")
			return 0
		df=ts.get_k_data(code,ktype=ktype1)
		df['code']=str(code)
		df['ktype']=str(ktype1)
		gxrq = datetime.datetime.now().strftime('%Y-%m-%d')
		gxsj = datetime.datetime.now().strftime('%H%M')
		df['gxrq']=gxrq
		df['gxsj']=gxsj
		return df
	#存入csv	
	def save_to_csv(self,code,df,mode):
		files1=self.get_csvmc(code)
		if mode=='a':
			df.to_csv(files1,mode='a',header=False)
			print('- 增量存入csv')
		else :
			df.to_csv(files1)
			print('- 覆盖存入csv')
		return 1
	#从本地取数
	def get_k_from_db(self,code,ktype1):
		files1=self.get_csvmc(code)
		if os.path.exists(files1):
			with open(files1,'r',encoding='utf-8') as csv_file:
				df = read_csv(csv_file,index_col=0)#指定0列为index列
		else:
			print('未找到股票数据，请先载入')
			if ktype1=='30':
				df=self.get_k_from_api(code,'m')
			else:
				df=self.get_k_from_api(code,ktype1)

			df.drop([len(df)-1],inplace=True)
			self.save_to_csv(code,df,'')
			return df#DataFrame([])
		return df[df.ktype==ktype1]
	#判断最后一条数据是否今天的
	def pd_last_k(self,df):
		#640  2020-03-25  14.550  14.300  14.600  ...   300414      D  2020-03-25  2349
		#210  2020-03-25  12.710  14.300  14.640  ...   300414      w  2020-03-25  2350
		#50  2020-03-25  12.370  14.300  15.370  ...   300414      m  2020-03-25  2350
		if df.empty:
			print("获取的数据 -Df-是空")
			return 0
		d_today = datetime.datetime.now().strftime('%Y-%m-%d')
		#如果是周六日，取周五
		df=df[-1:]
		d_last=df.values.tolist()[0][0]#最后一条记录的日期
		
		if d_today==d_last:
			return 1
		return 0
	def get_k(self,code,ktype1):
		
		#从本地取数的条件
			#最后一条数据是今天的
			#早上9点之前是前一天的数据
		df_bd=self.get_k_from_db(code,ktype1)
		if self.pd_last_k(df_bd)==1 and df_bd.empty is False:
			return df_bd
		#print(df_bd)
		#否则 从接口取数
		df_jk=self.get_k_from_api(code,ktype1)
		#30分钟线不做存储
		if ktype1=='30':
			return df_jk

		#写入数据库的条件
			#判断时间已到到15：00
			#判断最后一条数据是否今天的
		#print(df_jk)
		gxsj = datetime.datetime.now().strftime('%H%M')
		bd_date_li=df_bd.date.values.tolist()
		jk_date_li=df_jk.date.values.tolist()
		if df_jk.empty:return 0
		#最后一个时间删除，用于增量插入
		if ktype1 in ['w','m'] and len(jk_date_li)>0:
			jk_date_li.pop()
		if (int(gxsj)<1500 and int(gxsj)>930) and ktype1=='D' :
			jk_date_li.pop()
		
		#插入本地
		#判断最后一个时间一样

		#接口的数据不在本地，增量插入数据
		list_not_in=[]
		for d in jk_date_li:
			if d not in bd_date_li:
				list_not_in.append(d)

		if len(list_not_in)>0:
			print(list_not_in)
			df=df_jk[df_jk.date.isin(list_not_in)]
			self.save_to_csv(code,df,'a')
				
		return df_jk




#kk=gu_save('0')
#df=kk.get_k_from_api('300414','m')
#kk.save_to_csv('300414',df,'')
#df2=kk.get_k_from_api('300414','w')
#df=kk.get_k('603336','D')
#df=df.append(df2)
#print(df)
