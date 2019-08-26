#gupiaoClass
#股票类
import tushare as ts
import datetime
class gupiaoClass(object):
	"""docstring for gupiaoClass
		股票类
	"""
	def __init__(self, arg):
		super(gupiaoClass, self).__init__()
		self.arg = arg
		self.code=arg
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
		df=ts.get_today_all()
		print(df.head())
		return df

	#存储K线
	def save_k(self):
		pass

	#存储基础信息
	def save_jcxx(self):
		pass

	#删除K线
	def _delete_k(self):
		pass

	#判断是否一致K线
	def _issameK(self):
		pass

	#提取信息
	def select_k(self):
		pass
		
	def select_jcxx(self):
		pass
h=gupiaoClass('').get_day_all()