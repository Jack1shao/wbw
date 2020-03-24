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
	def get_day_all(self):

		gxrq = datetime.datetime.now().strftime('%Y-%m-%d')
		gxsj = datetime.datetime.now().strftime('%H:%M')
		df=ts.get_today_all()
		df['gxrq']=gxrq
		df['gxsj']=gxsj
		return df

	def download_stock_basic_info(self):
		#获取股票代码名称等基本信息，并写入数据库
		# code,代码
		# name,名称
		# industry,所属行业
		# area,地区
		# pe,市盈率
		# outstanding,流通股本
		# totals,总股本(万)		
		# totalAssets,总资产(万)
		# liquidAssets,流动资产
		# fixedAssets,固定资产
		# reserved,公积金
		# reservedPerShare,每股公积金
		# eps,每股收益
		# bvps,每股净资
		# pb,市净率
		# timeToMarket,上市日期
		list1=[]
		df = ts.get_stock_basics()
		max_timeToMarket=20200101
		for code,row in df.iterrows():
			#判断未上市的公司
			if row['timeToMarket']==0:
				list1.append(code)
		#删除未上市的公司记录
		df2=df.drop(list1,axis=0)
		return df2

	def download_stock_k_line_hist(code,ktypes):
		#获取股票k线
		 	#获取历史数据（前复权）get_h_data
		# 参数说明：
			# code:string,股票代码 e.g. 600848
			# start:string,开始日期 format：YYYY-MM-DD 为空时取当前日期
			# end:string,结束日期 format：YYYY-MM-DD 为空时取去年今日
			# autype:string,复权类型，qfq-前复权 hfq-后复权 None-不复权，默认为qfq
			# index:Boolean，是否是大盘指数，默认为False
			# retry_count : int, 默认3,如遇网络等问题重复执行的次数
			# pause : int, 默认 0,重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
		# 返回值说明：
			# date : 交易日期 (index)
			# open : 开盘价
			# high : 最高价
			# close : 收盘价
			# low : 最低价
			# volume : 成交量
			# amount : 成交金额
			#df=ts.get_h_data(code,start='2011-01-01', end='2017-03-16')
			#print(df)
		datestart='1990-01-01' #起始日期  #end=time.strftime('%Y-%m-%d',time.localtime(time.time()))#结束日期
		dateend=datetime.datetime.now().strftime('%Y-%m-%d')#结束日期
		#dateend='2017-03-16'#结束日期
		if get_kline_maxdate(code,ktypes)!=0:
			datestart=get_kline_maxdate(code,ktypes)[2]
		print(datestart,dateend,code,ktypes)
		df=ts.get_hist_data(code,ktype=ktypes,start=datestart,end=dateend)
		df['code']=str(code)
		df['ktype']=str(ktypes)
		return d