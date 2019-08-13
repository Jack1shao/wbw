#*************
#获取股票信息
#2017.04.07
#sjk
#*************
from sqlalchemy import create_engine
# from matplotlib.pylab import date2num
import tushare as ts
import pandas as pd
import pymysql;
import datetime;
import time;
# import matplotlib.pyplot as plt
# import matplotlib.finance as mpf
# from matplotlib.finance import quotes_historical_yahoo_ochl

# 取K线
def GET_KLINE(code,ktypes,datestart,dateend):
		
		#   ts.get_k_data() : 主要参数说明
		#   
		#code	#证券代码：	#支持沪深A、B股	#支持全部指数	#支持ETF基金
		#ktype	#数据类型：	#默认为D日线数据	#D=日k线 W=周 M=月 	#5=5分钟 15=15分钟 	#30=30分钟 60=60分钟
		#autype	#复权类型：	#qfq-前复权 hfq-后复权 None-不复权，默认为qfq
		#index	#是否为指数：	#默认为False	#设定为True时认为code为指数代码
		#start	#开始日期	#format：YYYY-MM-DD 为空时取当前日期
		#end	#结束日期 ：	#format：YYYY-MM-DD 
		
		#数据属性说明
		#date	#日期和时间	#低频数据时为：YYYY-MM-DD	#高频数为：YYYY-MM-DD HH:MM
		#open	#开盘价
		#close	#收盘价
		#high	#最高价
		#low	#最低价
		#volume	#成交量
		#code	#证券代码
	
		datestart='2017-01-04' #起始日期  注：日期太早get_k_data会出现错误
		dateend=datetime.datetime.now().strftime('%Y-%m-%d')#结束日期
		# 取月线和周线时应注意月尾和周末
		print(datestart,dateend,code,ktypes)
		df=ts.get_k_data(code,start=datestart, end=dateend,ktype=ktypes)

		df['code']=str(code)
		df['ktype']=str(ktypes)
		
		return df
def an(df):
	date0=[]
	date1=[]
	date2=[]
	
	
	# 取df的总行数，-1为下标为0开始
	# i=df.iloc[:,0].size-1
	count_up=0
	count_down=0 
	qs_up=0
	qs_down=0
	i=2
	qs=[]

	while i<df.iloc[:,0].size:
			print(df.loc[i,'date'])
			open0=df.loc[i,'open']
			close=df.loc[i,'close']
			high=df.loc[i,'high']
			low=df.loc[i,'low']
			open1=df.loc[i-1,'open']
			close1=df.loc[i-1,'close']
			high1=df.loc[i-1,'high']
			low1=df.loc[i-1,'low']
			open2=df.loc[i-2,'open']
			close2=df.loc[i-2,'close']
			high2=df.loc[i-2,'high']
			low2=df.loc[i-2,'low']
			# 变换重叠k线，分上涨和下跌两种
			if (high1>=high and low1<=low and open1<=close1):
				high=high1
				high1=open0
				if close1>open0: close1=open0
				
			if (high1>=high and low1<=low and open1>=close1):
				low=low1
				low1=open0
				if close1<open0: close1=open0
					

			
			#————————————
			#条件1：上涨
			
			up=0
			if (low>=low1 and high>=high1 and (open0<=close or open1<=close1)) :up=1
			if low<=low1 and high>=high1 and open0<=close:up=1
			if low<=low1 and high<=high1 and open0<=close and open1<=close1:up=1
			count_up=count_up+up
			print('判断上涨条件up=%d'%up)

			#条件2 下跌
			
			down=0
			if high1>=high and low1>=low and (open0>=close or open1 >=close1):down=1
			if high1<=high and low1>=low and open0>=close:down=1
			if high1<=high and low1<=low and open0>=close and open1>=close1:down=1
			count_down=count_down+down
			print('判断下跌条件down=%d'%down)
			#k线>4条形成趋势
			
			if count_down*count_up==0 and count_up+count_down>=4  :

				qs_up=count_up-count_down
				
				qs.append(df.loc[i-abs(qs_up)])
				print('判断趋势形成于%s'%df.loc[i-abs(qs_up),'date'],qs_up)
				# print(df.loc[i-abs(qs_up)-1])
			else:
			#若不能连续上涨清零
				count_up=count_up*up
				count_down=count_down*down
			# print(qs_up,count_up,count_down)
			if count_up>=1:
				s1='形成笔的要素'
				# print('%s上涨%s个周期'%(df.loc[i,'date'],count_up))
			# if count_up>0 and open2>close2  and open2>close1:print(df.loc[i,'date'],'底分型')
			# if count_down>=1:print('%s连续下跌%s个周期'%(df.loc[i,'date'],count_down))
			if count_up+count_down==0: 
				 print('错误',open1,close1,high1,low1,open0,close,high,low)

			#------------
			#循环条件控制
			
			i=i+1
	print(qs)
	



#函数：创建mysql链接

def mysql_create_engine():
	try:
		engine = create_engine("mysql+pymysql://root:123456@localhost:3306/stock?charset=utf8",encoding="utf-8", echo=True)
		print('create_engine succeeded')
	except Exception as e:
		print(str(e))
	return engine

#函数1：获取上市公司股票基本信息
def download_stock_basic_info():
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
	try:
		engine = mysql_create_engine()
		conn=engine.connect()#获取数据库链接，为执行sql准备
		print('get conn succeeded')
		sql='delete from stockbasic '#删除已获取股票代码（全部删除）。数据不多，简便方法，否则要用增量写入
		cur=conn.execute(sql)
		conn.close()
		list1=[]
		df = ts.get_stock_basics()
		max_timeToMarket=20170101
		for code,row in df.iterrows():
			#判断未上市的公司
			if row['timeToMarket']==0:
				list1.append(code)
		#删除未上市的公司记录
		df2=df.drop(list1,axis=0)
		print('create_engine succeeded')
		df2.to_sql('stockbasic',engine,if_exists='append') #追加到数据库表中
		print('stockbasic into mysql succeeded')
	except Exception as e:
		print(str(e));
	return 0
	
# 补全股票代码(6位股票代码)
# input: int or string
# output: string
def getSixDigitalStockCode(code):
	strZero = ''
	for i in range(len(str(code)), 6):
		strZero += '0'
	return strZero + str(code)

#函数 下载股票k线（日周月）get_hist_data（）

def download_stock_k_lineH(code):
	#获取股票k线
	# 参数说明：

	# code：股票代码，即6位数字代码，或者指数代码（sh=上证指数 sz=深圳成指 hs300=沪深300指数 sz50=上证50 zxb=中小板 cyb=创业板）
	# start：开始日期，格式YYYY-MM-DD
	# end：结束日期，格式YYYY-MM-DD
	# ktype：数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
	# retry_count：当网络异常后重试次数，默认为3
	# pause:重试时停顿秒数，默认为0、

	# 返回值说明：

	# date：日期
	# open：开盘价
	# high：最高价
	# close：收盘价
	# low：最低价
	# volume：成交量
	# price_change：价格变动
	# p_change：涨跌幅
	# ma5：5日均价
	# ma10：10日均价
	# ma20:20日均价
	# v_ma5:5日均量
	# v_ma10:10日均量
	# v_ma20:20日均量
	# turnover:换手率[注：指数无此项]
	try:
		engine = mysql_create_engine()
		df=ts.get_hist_data(code)#日k线
		df['code']=code
		df['ktype']='d'
		#df.to_sql('stockkline',engine,if_exists='append')
		df=ts.get_hist_data(code,ktype='W')#周K线
		df['code']=code
		df['ktype']='w'
		#df.to_sql('stockkline',engine,if_exists='append')
		df=ts.get_hist_data(code,ktype='m')#月k线
		df['code']=code
		df['ktype']='m'
		print(df)
		#df.to_sql('stockkline',engine,if_exists='append')
		print('stockkline into mysql succeeded')
		
	except Exception as e:
		print(str(e));
	return df
	
#函数 取公司的代码、名称、上市日期
def get_stock_name(code):
	try:
		start=''
		engine = mysql_create_engine()
		conn=engine.connect()
		print('get conn succeeded')
		sql='select code,name,timeToMarket from stockbasic where code=%s'%(code)#获取股票代码，名称和上市日期
		cur=conn.execute(sql)
		datelist=cur.fetchall()
		dateretun=[]
		if len(datelist)!=1:return 0
		for row in datelist:  
			dateretun.append(row[0])
			dateretun.append(row[1])
			start=row[2][0:4]+'-'+row[2][4:6]+'-'+row[2][6:8]#转换上市日期
			dateretun.append(start)
		#print(dateretun)
		conn.close()
	except Exception as e:
		print(str(e));
	return dateretun

#函数 取K线最大日期，实现增量下载
def get_kline_maxdate(code,ktype):
	dateretun=[]
	try:
		engine = mysql_create_engine()
		conn=engine.connect()
		print('get conn succeeded')
		sql2="select code,max(date) from stockklinehist where code=%s and ktype='%s' "%(str(code),str(ktype))
		cur=conn.execute(sql2)
		datelist=cur.fetchall()
		conn.close()
		#获取数据：code ktype max(date)
		#这里还要判断当天未完成的数据不能写入数据库
		
		for row in datelist:
			#返回空值判断
			if row[0] is None:return 0
			dateretun.append(code)
			dateretun.append(ktype)
			print(row[1])
			datess=row[1]+datetime.timedelta(days =1)#加一天，根据函数的起始日期的要求
			dateretun.append(datess.strftime('%Y-%m-%d'))#r日期格式化
		print(dateretun)
		#conn.close()
	except Exception as e:
		print(str(e));
	return dateretun
	
	
	
	#函数 增量获取历史K线 download_stock_k_line_zl
def download_stock_k_line_zl(code,ktypes):
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
	# 返回值说明：qu'sh
		# date : 交易日期 (index)
		# open : 开盘价
		# high : 最高价
		# close : 收盘价
		# low : 最低价
		# volume : 成交量
		# amount : 成交金额
	try:
		#df=ts.get_h_data(code,start='2011-01-01', end='2017-03-16')
		#print(df)
		datestart='1990-01-01' #起始日期  #end=time.strftime('%Y-%m-%d',time.localtime(time.time()))#结束日期
		dateend=datetime.datetime.now().strftime('%Y-%m-%d')#结束日期
		#dateend='2017-03-16'#结束日期
		#增量取数 取数据库中已有数据日期最大值
		if get_kline_maxdate(code,ktypes)!=0:
			datestart=get_kline_maxdate(code,ktypes)[2]

		print(datestart,dateend,code,ktypes)

		df=ts.get_hist_data(code,ktype=ktypes,start=datestart,end=dateend)
		df['code']=str(code)
		df['ktype']=str(ktypes)
		print(df)
		# engine = mysql_create_engine()
		# df.to_sql('stockklinehist',engine,if_exists='append')
		#time.sleep(1)
		print('stockklinehist into mysql succeeded')
		print('***try is end*')
		return df
	except Exception as e:
		print(str(e));
	return 0
	
#函数 取K线
def down_all_kline():
	#函数 取公司的代码、名称、上市日期
	try:
		start=''
		engine = mysql_create_engine()
		conn=engine.connect()
		print('数据库链接成功180052')
	
		sql='select code,name,timeToMarket from stockbasic order by code'#获取股票代码，名称和上市日期
		cur=conn.execute(sql)
		datelist=cur.fetchall()
		
		# dateretun=[]
		# list_ktyp=['w','d','m']
		list_ktyp=['m']
		for row in datelist: 
			for ty in list_ktyp:
				#code=str(row[0])
				df=download_stock_k_line_zl(row[0],ty[0])
				#print(code)
			# time.sleep(1)
		conn.close()
		print('数据库链接关闭180052')
	except Exception as e:
		print(str(e));
	return 0
#函数：临时获取K线图，并对k线进行分析
def get_kline_list():
	#主要参数说明
	#code	#证券代码：	#支持沪深A、B股	#支持全部指数	#支持ETF基金
	#ktype	#数据类型：	#默认为D日线数据	#D=日k线 W=周 M=月 	#5=5分钟 15=15分钟 	#30=30分钟 60=60分钟
	#autype	#复权类型：	#qfq-前复权 hfq-后复权 None-不复权，默认为qfq
	#index	#是否为指数：	#默认为False	#设定为True时认为code为指数代码
	#start	#开始日期	#format：YYYY-MM-DD 为空时取当前日期
	#end	#结束日期 ：	#format：YYYY-MM-DD 
	
	#数据属性说明
	#date	#日期和时间	#低频数据时为：YYYY-MM-DD	#高频数为：YYYY-MM-DD HH:MM
	#open	#开盘价
	#close	#收盘价
	#high	#最高价
	#low	#最低价
	#volume	#成交量
	#code	#证券代码
	data_list = []
	hist_data=ts.get_k_data('000001',start='2017-01-01', end='2017-03-16')
	yestd=[]
	for dates,row in hist_data.iterrows():
		# 将时间转换为数字
		date_time = datetime.datetime.strptime(row[0],'%Y-%m-%d')
		t = date2num(date_time)
		#将dateframe转为List
		open,high,low,close = row[1:5]
		datas = (t,open,high,low,close)
		data_list.append(datas)
	return data_list
#函数：画股票k线图
def draw_kline(data_list):
	# 创建子图
	fig, ax = plt.subplots()
	fig.subplots_adjust(bottom=0.2)
	# 设置X轴刻度为日期时间
	ax.xaxis_date()
	plt.xticks(rotation=45)
	plt.yticks()
	plt.title("code=%s",)
	plt.xlabel("date")
	plt.ylabel('yun')
	mpf.candlestick_ochl(ax,data_list,width=0.8,colorup='red',colordown='green')
	#plt.grid()##'''
	plt.show()
	return 0

	#测试

an(GET_KLINE('002185','M','',''))
#download_stock_basic_info()
#download_stock_k_line_zl('600848','M')
#get_stock_name('600848')
#get_kline_maxdate('000002','d')
#draw_kline(get_kline_list());
# down_all_kline()
#download_stock_k_lineH('300301')




