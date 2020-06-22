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
from cciorder import dmiorder
from operClass import csv_op

Stock=namedtuple('Stock','code name hangye totals')

#获取数据的接口类
class jiekou:
	def getbasc(self,code1):
		df= self.get_base_from_api()
		df=df[df.index==code1]
		return df

	def getallstock(self,code1list):

		csv_path='d:/stock_csv/{}.csv'.format('basc')
		if 'all' in code1list:print('获取所有Stock')
		jk=csv_op()
		df=jk.get_from_csv(csv_path)
		st_list=[]
		co_list=df.index.values.tolist()

		for co in co_list:
			s_code=getSixDigitalStockCode(co)
		
			if s_code not in code1list and 'all' not in code1list:
				continue
			s_name=df[df.index==co].name.values[-1]
			s_totals=df[df.index==co].totals.values[-1]
			s_hy=df[df.index==co].industry.values[-1]
			s=Stock(code=s_code,name=s_name,hangye=s_hy,totals=s_totals)
			st_list.append(s)
		return st_list

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
	#基础数据2
	def get_base_from_db(self):
		basc='basc'
		files1=self.get_csvmc(basc)
		if os.path.exists(files1):
			with open(files1,'r',encoding='utf-8') as csv_file:
				df = read_csv(csv_file,index_col=0)#指定0列为index列
		return df
		
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
	def dmi(self):
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
	'''策略1----背驰8 bc8'''
	def dueorder(self):
		a,b,c=self.bc()
		cn1=a>0#最后一个顶背驰

		if cn1 and (c-b) in [7]:
			return 1
		return 0
#策略2----背驰 9
class ccibc9(cciorder):
	'''策略2----背驰9 bc9'''
	def dueorder(self):
		a,b,c=self.bc()
		cn1=a>0#最后一个顶背驰

		if cn1 and (c-b) in [8]:
			return 1
		return 0
#策略3----macd红柱
class macdyxhz(macdorder):
	'''策略3----macd红柱 yhz'''
	def dueorder(self):
		macd=self.macd3()
		if macd>0:
			return 1
		return 0
#策略4----dmi横盘或高于80
class dmi50(dmiorder):
	'''策略4----高于50(向上趋势中) d50'''
	def dueorder(self):
		PDI,MDI,ADX,ADXR=self.dmi3()
		
		a2dx=ADX[-2:]
		#条件
		n1=MDI[-1]<20
		n2=a2dx[0]<a2dx[1]
		n3=a2dx[1]>50
		n4=PDI[-1]>21
		if n1 and n4 and n2 and n3:
			return 1
		return 0
#策略5----30日红盘占比
#策略6----量能放大
#策略7----9日涨幅幅榜

#管理策略的类
class Context:
	'''管理策略的类'''
	def __init__(self,csuper):
		self.csuper = csuper
	def GetResult(self):
		return self.csuper.dueorder()

#股票代码补齐
def getSixDigitalStockCode(code):
		strZero = ''
		for i in range(len(str(code)), 6):
			strZero += '0'
		return strZero + str(code)
#函数--根据代码获取单个基础信息
def getstockbasics(code1):
	
	'''函数--根据代码获取单个基础信息'''

	jk=jiekou()
	df=jk.getbasc(code1)[-1:]
	if df.empty:
		print('没有该代码{}的信息'.format(code1))
		return None 
	s_code=df.index.values[-1]
	s_name=df.name.values[-1]
	s_totals=df.totals.values[-1]
	s_hy=df.industry.values[-1]
	s=Stock(code=s_code,name=s_name,hangye=s_hy,totals=s_totals)
	return s   #返回一个Stock 

#函数--根据代码获取单个策略
def getorderresult(s):
	'''函数--根据代码获取单个策略'''
	#s=getstockbasics(code1)
	print (getstockbasics.__doc__,s)
	code1=s.code
	#获取k线记基础指标
	szb=stockzb(s)
	m=m_kl()#月线修饰
	w=w_kl()#周线修饰
	d=D_kl()#日线修饰
	hf=Hf_kl()#30线修饰


	#print(szb.df)

	#应用策略
	#1--日线策略
	szb.decorator(d)#日线修饰
	szb.getk()#获取k线
	strategy = {}
	strategy[1] = Context(ccibc8(szb))
	strategy[2] = Context(ccibc9(szb))
	strategy[3] = Context(dmi50(szb))
	code_order=[]

	for i in range(1,len(strategy)+1):
		x=strategy[i].GetResult()
		y=strategy[i].csuper.__doc__
		str_d=y if x else '00'
		if x:code_order.append([code1,s.name,x,str_d])


	#2--月线策略
	
	szb.decorator(m)#月线修饰
	szb.getk()#获取月线
	
	strategy = {}
	strategy[1] = Context(macdyxhz(szb))

	for i in range(1,len(strategy)+1):
		x=strategy[i].GetResult()
		y=strategy[i].csuper.__doc__
		str_d=y if x else '00'
		if x:code_order.append([code1,s.name,x,str_d])
	#print(szb.df.head())
	return code_order

#函数--获取给点集合代码所有策略
def get_all_orderresult():
	'''函数--获取给点集合代码所有策略'''
	order_js_list=[]
	tt=[]
	jk=jiekou()
	

	#大名单列表存入tt
	op=csv_op()
	dmd_li1=op.get_txt('sv_dmd1.csv').code.values.tolist()
	for code in dmd_li1:
		co=getSixDigitalStockCode(code)
		tt.append(co)

	#tt=['600359','600609','002498',	'002238','300415','000987',	'600598','000931']#tt=['all']
	st_list=jk.getallstock(tt)#获取符合的代码Stock，，tt=['all']
	#容错
	if len(st_list)==0:
		print('没有符合的代码')
		return 0
	
	
	#获取所有策略结果
	for s in st_list:
		jg_li=getorderresult(s)#获取策略结果
		order_js_list.extend(jg_li)#集合所有结果

	#结果集存入order.csv
	df=DataFrame(order_js_list,columns=[ 'code', 'name','cl','clname'])
	df.to_csv('order.csv')
	
	return 0
#函数 ---分离策略结果集
def fl_ordercsv():
	'''函数 ---分离策略结果集'''
	op=csv_op()
	cl_df=op.get_txt('order.csv')
	#策略名去重
	clname_li11=cl_df.clname.values.tolist()
	clname_li=(list(set(clname_li11)))
	
	for na in clname_li:
		files1='{}.txt'.format(na[-3:])
		df=cl_df[cl_df.clname==na]
		df.to_csv(files1)

	return 0

if __name__ == '__main__':
	#输入股票代码获取该代码的基础信息
	#l=getorderresult('000931')
	print(get_all_orderresult.__doc__)
	#get_all_orderresult()
	print(fl_ordercsv.__doc__)
	#fl_ordercsv()