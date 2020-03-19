#gupiaoClass
#股票类
import tushare as ts
import datetime
import csv
import os
from pandas import read_csv
class gupiaoClass(object):
	"""docstring for gupiaoClass
		股票类
		得到
	"""
	def __init__(self, arg):
		super(gupiaoClass, self).__init__()
		self.arg = arg
		self.code=str(arg)
		self.filepath='e:/stock_k/{}.csv'.format(self.code)
		print(arg)
	#获取股票基础信息
	def get_jcxx(self):
		df = ts.get_stock_basics()
		#print(df)
		return df

	#获取股票历史k线
	def get_k(self,code1,ktypes,datestart,dateend):
		'''	
			#   ts.get_k_data() : 主要参数说明
					# 
					#code	#证券代码：	#支持沪深A、B股	#支持全部指数	#支持ETF基金
					#ktype	#数据类型：	#默认为D日线数据	#D=日k线 W=周 M=月 	#5=5分钟 15=15分钟 	#30=30分钟 60=60分钟
					#autype	#复权类型：	#qfq-前复权 hfq-后复权 None-不复权，默认为qfq
					#index	#是否为指数：	#默认为False	#设定为True时认为code为指数代码
					#start	#开始日期	#format：YYYY-MM-DD 为空时取当前日期
					#end	#结束日期 ：	#format：YYYY-MM-DD 
		'''
		code=str(self.code)
		datestart='2018-05-04' 
		#起始日期 注：日期太早get_k_data会出现错误
		now = datetime.datetime.now()
		#加一天
		delta = datetime.timedelta(days=1)
		n_days=now+delta
		dateend=n_days.strftime('%Y-%m-%d')#结束日期
		# 取月线和周线时应注意月尾和周末
		# print(datestart,dateend,code,ktypes,'取得k线')
		if ktypes=='D':
			df=ts.get_k_data(code)
		else:
			df=ts.get_k_data(code,start=datestart, end=dateend,ktype=ktypes)
		#df=ts.get_hist_data(code,start=datestart, end=dateend,ktype=ktypes)
		df['code']=str(code)
		df['ktype']=str(ktypes)
		#容错
		if len(df)==0:
			print("没有数据")
			return []		
		#print(df)
		return df
	#当天的数据
	def get_day_all(self):
		filepath_today="e:/stock_k/today_all.csv"
		
		now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

		df=ts.get_today_all()
		df['date']=now
		df['name']=''
		df.to_csv(filepath_today,encoding="gbk")

		return 0

	#存储K线
	def save_k(self,df):
		#filepath='e:/stock_k/{}.csv'.format(self.code)
		print(self.filepath)
		df.to_csv(self.filepath)
		return 1
	#增量存储k线
	def save_k_append(self,df):
		#
		df.to_csv(self.filepath,mode='a', header=None)
		return 1

	#存储基础信息
	def save_jcxx(self,df):
		filepath_jcxx="e:/stock_k/jcxx.csv"
		df.to_csv(filepath_jcxx,encoding='utf-8')
		return 1

	#删除K线
	def _delete_k(self):
		pass

	#判断是否一致K线
	def _issameK(self):
		pass

	#提取信息
	def select_k(self):
		if os.path.exists(self.filepath):
			
			with open(self.filepath, 'r') as csv_file:
				df = read_csv(csv_file,header=0)

		else:return 0

		return df
	#提取基础信息	
	def select_jcxx(self):
		filepath_jcxx="e:/stock_k/jcxx.csv"
		if os.path.exists(filepath_jcxx):
			
			with open(filepath_jcxx, 'r',errors='ignore') as csv_file:
				df = read_csv(csv_file,header=0)
		else:return 0
		for x in df.iterrows():
			print(x)
			
		return df
	def  select_today_k(self):
		filepath_jcxx="e:/stock_k/today_all.csv"
		if os.path.exists(filepath_jcxx):
			
			with open(filepath_jcxx, 'r',errors='ignore') as csv_file:
				df = read_csv(csv_file,header=0,encoding="gbk")
		else:return 0
		for row in df.iterrows():
			print(row)
		
		
#h=gupiaoClass('300377')
#h.get_day_all()
#df=(h.get_k('002340','D','2019-01-01','2019-08-01'))
#h.save_k(df)
#h.save_jcxx(h.get_jcxx())
#h.select_k()
#h.select_today_k()
#h.select_jcxx()
#print(os.listdir('e:/stock_k/'))
