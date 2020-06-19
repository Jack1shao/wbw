#stockmd.py
#基础
import os
from pandas import read_csv
from abc import ABCMeta, abstractmethod
from pandas.core.frame import DataFrame
import talib
import tushare as ts
import datetime
from collections import namedtuple

Stock=namedtuple('Stock','code name hangye totals')

#获取数据的接口类
class jiekou:
	def getbasc(self):
		return self.get_base_from_api()
	def getkl(self,code,ktype1):
		return self.get_k_from_csv(code,ktype1)
		
		
	def get_csvmc(self,code):
		csv_path='d:/stock_csv/{}.csv'.format(code)
		return csv_path
	#从本地取数
	def get_k_from_csv(self,code,ktype1):
		print('来自{2}类--从本地取-{0}-{1}'.format(code,ktype1,self.__class__.__name__))
		files1=self.get_csvmc(code+ktype1)
		if os.path.exists(files1):
			with open(files1,'r',encoding='utf-8') as csv_file:
				df = read_csv(csv_file,index_col=0)#指定0列为index列
		else:
			print('未找到股票数据，请先载入')
			return DataFrame([])
		return df
	#从接口取数
	def get_k_from_api(self,code1,ktype1):
		print('来自{2}类 从api取-{0}-{1}'.format(code1,ktype1,self.__class__.__name__))
		code=str(code1)
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
	#基础数据1
	def get_base_from_api(self):
		
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

		
#股---实体类
class stockzb(object):
	"""docstring for stockclass"""
	def __init__(self, stock):
		super(stockzb, self).__init__()
		#参数为股票代码
		self.stock = stock
		#k线数据
		self.df=None
	
	#修饰器函数
	def decorator(self,component):
		self.component=component

	#获取股票代码
	def getcode(self):
		return self.stock.code

	#获取股票名称
	def getname(self):
		return self.stock.name
		

	#市值，根据日线
	def get_sz(self):
		jiage=self.df[-1:].close.values.tolist()
		sz=self.totals*jiage[0]
		#print(float('%.2f' % sz),'亿')#小数位数
		return float('%.2f' % sz)

	def getk(self):
		print('来自{}类--获取股票k线'.format(self.__class__.__name__))
		self.df=self.component.getk(self.stock.code)
		return self.df


	def macd(self):
		df=self.df
		diff,dea,macd3=talib.MACD(df['close'],fastperiod=12, slowperiod=26, signalperiod=9)
		return diff,dea,macd3
	#指标boll
	def boll(self):
		df=self.df
		up,mid,lo=talib.BBANDS(df.close,timeperiod=20,nbdevup=2,nbdevdn=2,matype=0)
		return up,mid,lo
	#指标dmi
	def dmi(self,df):
		df=self.df
		MINUS_DI=talib.MINUS_DI(df.high,df.low,df.close,timeperiod=14)
		PLUS_DI = talib.PLUS_DI(df.high,df.low,df.close, timeperiod=14)
		ADX = talib.ADX(df.high,df.low,df.close, timeperiod=6)
		ADXR = talib.ADXR(df.high,df.low,df.close, timeperiod=6)
		return PLUS_DI.tolist(),MINUS_DI.tolist(),ADX.tolist(),ADXR.tolist()
	#指标ma
	def ma(self):
		df=self.df
		closed=df['close'].values
		sma=talib.MA(closed,timeperiod=34,matype=0)
		return sma.tolist()
	#指标cci
	def cci(self):
		#def CCI(df, n):
		#  PP = (df['high'] + df['low'] + df['close']) / 3
		#CCI = pd.Series((PP - pd.rolling_mean(PP, n)) / pd.rolling_std(PP, n) / 0.015, name = 'CCI' + str(n))
		#return CCI
		df=self.df
		cci=talib.CCI(df.high,df.low,df.close, timeperiod=14)
		return cci.tolist()
		
#装饰类
class Finery():
	def __init__(self):
		self.component=None

	def decorator(self,component):
		self.component=component

	__metaclass__=ABCMeta

	@abstractmethod
	def getk(self,code1):
		if self.component:
			self.component.getk(self)

#月@
class m_kl(Finery):
	def getk(self,code1):
		Finery.getk(self,code1)
		print('m_kl12'+code1)
		g=jiekou()
		df=g.getkl(code1,'m')
		return df
#周@
class w_kl(Finery):
	def getk(self,code1):
		Finery.getk(self,code1)
		g=jiekou()
		df=g.get_k_from_csv(code1,'w')
		return df
#日@
class D_kl(Finery):
	def getk(self,code1):
		Finery.getk(self,code1)
		g=jiekou()
		df=g.get_k_from_csv(code1,'D')
		return df
#hf@
class Hf_kl(Finery):
	def getk(self,code1):
		Finery.getk(self,code1)
		g=jiekou()
		df=g.get_k_from_csv(code1,'30')
		if df.empty:
			df=g.get_k_from_api(code1,'30')
		return df




		
#命令
class commandclass(object):
	"""docstring for commandclass"""
	def __init__(self, arg):
		super(commandclass, self).__init__()
		self.arg = arg
		

#策略
class celvclass(object):
	"""docstring for celvclass"""
	def __init__(self, arg):
		super(celvclass, self).__init__()
		self.arg = arg
	
	def bc9():
		pass

	def rs100():
		pass

if __name__ == '__main__':
	s=Stock(code='002498',name='hanl',hangye='xd',totals='2000')
	szb=stockzb(s)
	
	m=m_kl()
	w=w_kl()
	d=D_kl()
	hf=Hf_kl()

	szb.decorator(m)

	szb.getk()
	print(szb.df)


	#print(s.getname())
