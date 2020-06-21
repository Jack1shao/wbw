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
from cciorder import cciorder
from cciorder import macdorder

Stock=namedtuple('Stock','code name hangye totals')

#获取数据的接口类
class jiekou:
	def getbasc(self,code1):
		df= self.get_base_from_api()
		df=df[df.index==code1]
		return df

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
		print('月线+'+code1)
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


#cciorder 为cci策略
#macd 为macd策略
#策略1----背驰 8
class ccibc8(cciorder):
	#策略1----背驰 8
	def dueorder(self):
		a,b,c=self.bc()
		cn1=a>0#最后一个顶背驰

		if cn1 and (c-b) in [7]:
			return 1
		return 0
#策略2----背驰 9
class ccibc9(cciorder):
	#策略2----背驰 9
	def dueorder(self):
		a,b,c=self.bc()
		cn1=a>0#最后一个顶背驰

		if cn1 and (c-b) in [8]:
			return 1
		return 0
#策略3----macd红柱
class macdyxhz(macdorder):
	#策略3----macd红柱
	def dueorder(self):
		macd=self.macd3()
		if macd>0:
			return 1
		return 0
#策略4----dmi横盘或高于80

#策略5----30日红盘占比
#策略6----量能放大
#策略7----9日涨幅幅榜

#管理策略的类
class Context:
	#管理策略的类
	def __init__(self,csuper):
		self.csuper = csuper
	def GetResult(self):
		return self.csuper.dueorder()

		

		


#函数--根据代码获取单个基础信息
def getstockbasics(code1):
	jk=jiekou()
	df=jk.getbasc(code1)[-1:]
	if df.empty:
		return None 
	s_code=df.index.values[-1]
	s_name=df.name.values[-1]
	s_totals=df.totals.values[-1]
	s_hy=df.industry.values[-1]
	s=Stock(code=s_code,name=s_name,hangye=s_hy,totals=s_totals)
	return s   #返回一个Stock 



	
if __name__ == '__main__':
	#输入股票代码获取该代码的基础信息
	s=(getstockbasics('600609'))
	print (s)
	#s=Stock(code='002498',name='hanl',hangye='xd',totals='2000')
	#获取k线记基础指标

	szb=stockzb(s)
	m=m_kl()
	w=w_kl()
	d=D_kl()
	hf=Hf_kl()

	szb.decorator(m)#月线修饰
	szb.getk()#获取月线

	#print(szb.df)

	#ccio=cciorder(szb)
	#print(ccio.bc9())
	#print(order(szb,cciorder))
	#应用策略
	cl1=Context(macdyxhz(szb))
	print(cl1.GetResult())


	#print(s.getname())
