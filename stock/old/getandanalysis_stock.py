#*************
#获取股票信息
#2017.04.07

#sjk
#*************
from sqlalchemy import create_engine
from matplotlib.pylab import date2num
import tushare as ts
import pandas as pd
import pymysql;
import datetime;
import time;
#import matplotlib as plt
#import matplotlib.finance as mpf
#from matplotlib.finance import quotes_historical_yahoo_ochl

#函数：创建mysql链接
#创建数据库连接引擎
def mysql_create_engine():
	try:
		engine = create_engine("mysql+pymysql://root:123456@localhost:3306/stock?charset=utf8",encoding="utf-8", echo=True)
		print('创建数据库连接引擎')
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

		sql='delete from stockbasic '#删除已获取股票代码（全部删除）。数据不多，简便方法，否则要用增量写入
		cur=conn.execute(sql)
		conn.close()
		list1=[]
        
		df = ts.get_stock_basics()
		max_timeToMarket=20200101
		for code,row in df.iterrows():
			#判断未上市的公司
			if row['timeToMarket']==0:
				list1.append(code)
		#删除未上市的公司记录
		df2=df.drop(list1,axis=0)

		df2.to_sql('stockbasic',engine,if_exists='append') #追加到数据库表中

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
def download_stock_k_line_zl(engine,code,ktypes):
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
	try:
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
		
		#engine = mysql_create_engine()
		df.to_sql('stockklinehist',engine,if_exists='append')
		time.sleep(1)
		print('stockklinehist into mysql succeeded')
		print('***try is end*')
		
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
		list_ktyp=['w','d','m']
		#list_ktyp=['w']
		print(datelist)
		stock_li=['300106','603336','300414','002498','300011','002335','002483','600598','002385','603019','300179','600120','300316','000725','600745','300346','300377','002216','600143','600804','300048','300215','002519','300131','300040','300370','600405','601126','600359','002777','300360','300259','002296','300095']
		for row in stock_li: 
			for ty in list_ktyp:
				code=str(row)
				download_stock_k_line_zl(engine,code,ty[0])
				print(code)

			time.sleep(1)
			
		conn.close()
		print('数据库链接关闭180052')
	except Exception as e:
		print(str(e));
	return 0
#函数：临时获取K线图，并对k线进行分析
def get_kline_list():
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
#download_stock_basic_info()
#download_stock_k_line_zl('600848','M')
#get_stock_name('600848')
#get_kline_maxdate('000002','d')
#draw_kline(get_kline_list());
down_all_kline()
#download_stock_k_lineH('300301')



