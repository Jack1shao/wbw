#
import tushare as ts
import datetime

class getstock(object):
	"""docstring for getstock
		获取单只股票信息
	"""
	def __init__(self, arg):
		super(getstock, self).__init__()
		self.arg = arg
		#股票代码
		self.code=str(arg)

	#获取股票名称
	def GET_BASE(self):

		df = ts.get_stock_basics()
		name=None
		if self.code=='today_all':return 'today_all'
		for c,row in df.iterrows():
			if str(c)==self.code:
				name=row['name']
		#容错
		if name==None:
			print("没有这只股票")
			return 0

		return name
	#获取股票k线
	# 月线，周线，日线，30分钟线
	def GET_KLINE(self,code1,ktypes,datestart,dateend):		
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
		if code=='today_all':return(self.__get_day_all())
		if len(code)!=6:
			print('股票代码错误')
			return 0
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
		gxrq = datetime.datetime.now().strftime('%Y-%m-%d')
		gxsj = datetime.datetime.now().strftime('%H:%M')
		df['gxrq']=gxrq
		df['gxsj']=gxsj
		#容错
		if len(df)==0:
			print("没有数据")
			return 0		
		#print(df)
		return df
	#获取当天所有股票信息
	def __get_day_all(self):

		gxrq = datetime.datetime.now().strftime('%Y-%m-%d')
		gxsj = datetime.datetime.now().strftime('%H:%M')
		df=ts.get_today_all()
		df['gxrq']=gxrq
		df['gxsj']=gxsj
		return df
