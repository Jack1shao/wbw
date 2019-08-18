#*************
#获取股票信息
#2017.04.07
#sjk
#*************
from sqlalchemy import create_engine
import tushare as ts
import pandas as pd
import pymysql;
import datetime;
import time;


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
	
	
		datestart='2018-05-04' #起始日期  注：日期太早get_k_data会出现错误
		dateend=datetime.datetime.now().strftime('%Y-%m-%d')#结束日期
		# 取月线和周线时应注意月尾和周末
		# print(datestart,dateend,code,ktypes)
		df=ts.get_k_data(code)
		#df=ts.get_hist_data(code,start=datestart, end=dateend,ktype=ktypes)
		# print(df)
		df['code']=str(code)
		df['ktype']=str(ktypes)
		i=df.loc[:,'date'].size-1

		# print(i,df.loc[df.loc[:,'date'].size-1,'date'])

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
				
		# #————————————
		# #条件1：上涨
		
		up=0
		if (low>=low1 and high>=high1 and (open0<=close or open1<=close1)) :up=1
		if low<=low1 and high>=high1 and open0<=close:up=1
		if low<=low1 and high<=high1 and open0<=close and open1<=close1:up=1
		# count_up=count_up+up
		# print('判断上涨条件up=%d'%up)

		# #条件2 下跌
		
		down=0
		if high1>=high and low1>=low and (open0>=close or open1 >=close1):down=1
		if high1<=high and low1>=low and open0>=close:down=1
		if high1<=high and low1<=low and open0>=close and open1>=close1:down=1
		# count_down=count_down+down
		# print('判断下跌条件down=%d'%down)
		if(open2>close2 and open2>close1 and up==1):
			# print(code,df.loc[df.loc[:,'date'].size-1,'date'])
			return 1
		else: return 0
		
def get_code():
	df = ts.get_stock_basics()
	# print(df)
	max_timeToMarket=20170101
	list1=[]
	ii=0
	for code,row in df.iterrows():
		#判断未上市的公司
		ii=ii+1
		if row['timeToMarket']>0 and row['timeToMarket']<20150101:
			if GET_KLINE(code,0,0,0)>0:
				print(code,row['name'],row['timeToMarket'],ii)
	

#函数：创建mysql链接

get_code()
# GET_KLINE('002292','D','','')
#download_stock_basic_info()
#download_stock_k_line_zl('600848','M')
#get_stock_name('600848')
#get_kline_maxdate('000002','d')
#draw_kline(get_kline_list());
# down_all_kline()
#download_stock_k_lineH('300301')




