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
from operClass import file_op

Stock=namedtuple('Stock','code name hangye totals')

#策略类
class bollorder:
	def __init__(self,stockzb):
		self.stockzb=stockzb
	def boll3(self):
		'''函数--所有股价在中轨之上，有连续3天以上下跌'''
		ii=6
		df=self.stockzb.df
		close_li=df.close.values.tolist()[-ii:]
		open_li=df.open.values.tolist()[-ii:]
		up,mid,lo=self.stockzb.boll()

		mid_li=mid.tolist()[-ii:]
		#在中轨之上
		c=-1
		c_day=0
		for i in range(0,ii):
			if close_li[i]<mid_li[i]:
				return 0
			if close_li[i]>open_li[i]:
				c=-1
				c_day=0

			if close_li[i]<open_li[i] :
				c_day+=1
				c=1
			if c_day>3:
				return c_day
			#print(close_li[i],open_li[i],mid_li[i],c,c_day)
		return  0

class macdorder:
	"""docstring for macdorder"""
	def __init__(self,stockzb):

		self.stockzb=stockzb
	
	def macd3(self):
		diff,dea,macd3=self.stockzb.macd()
		macd=macd3.tolist()
		return macd[-1]

		
class dmiorder:
	def __init__(self,stockzb):
		self.stockzb=stockzb

	def dmi3(self):
		PDI,MDI,ADX,ADXR=self.stockzb.dmi()
		return PDI,MDI,ADX,ADXR
		
class cciorder:
	def __init__(self,stockzb):

		self.df=stockzb.df
		self.cci=stockzb.cci()

	#cci折角1、判断
	def __cci_ana_updown(self,c1,c2,c3):
		if c2>c1 and c2>c3:return 1
		if c2<c1 and c2<c3:return -1
		return 0
	#强弱分界点
	def cci_ana_qrfj(self,cci1):
		bz1=0
		cciqrfj=[]
		total=len(cci1)
		js_up=1

		for i in range(0, total):
			if cci1[i]>100:
				bz1=1
			if cci1[i]<-100:
				bz1=-1
			if bz1>0:
				cciqrfj.append(js_up)
			else:
				cciqrfj.append(-100)
		return cciqrfj
	#强弱区域块
	def cci_qr_blok(self):
		'''cciorder类--强弱区域块'''
		cci_blok=[]#用于存储区域的起始和终止序号,是否强势，时间、空间和量能 三个维度，[600,630,'qs','30-len','30%','32320']
		cci1=self.cci
		high1=self.df.high.values.tolist()
		low=self.df.low.values.tolist()
		#两个状态值，当两个状态值不一致时，说明状态发生变化。
		bz0=0
		bz1=0
		cciqrfj=[]
		total=len(cci1)
		js_up=1

		for i in range(0, total):

			if cci1[i]>100:
				bz1=1

			if cci1[i]<-100:
				bz1=-1

			if len(cciqrfj)>0 and bz1!=bz0 :

				start=cciqrfj[0]
				end=cciqrfj[-1]
				#开始取该段的最高价和最低价
				hi_list=[]
				lo_list=[]
				for x in range(start,end+1):
					hi_list.append(high1[x])
					lo_list.append(low[x])
				max1=max(hi_list)
				min1=min(lo_list)
				kj=(max1-min1)/min1#振幅
				cci_blok.append([start,end,bz0,len(cciqrfj),float('%.2f'%kj)])
				cciqrfj=[]

			cciqrfj.append(i)

			if i==total-1:
				start=cciqrfj[0]
				end=cciqrfj[-1]
				#开始取该段的最高价和最低价
				hi_list=[]
				lo_list=[]
				for x in range(start,end+1):
					hi_list.append(high1[x])
					lo_list.append(low[x])
				max1=max(hi_list)
				min1=min(lo_list)
				
				kj=(max1-min1)/min1#振幅
				cci_blok.append([start,end,bz0,bz0,len(cciqrfj),float('%.2f'%kj)])
				cciqrfj=[]

			bz0=bz1
			#块[630, 639, 1, 1, 10, 0.23]]
		return cci_blok

	#区块形态
	
	#冲顶的形态(小丁与大定)
	def chongding(self):
		#顶点是否涨停，与高点的距离，分小丁与大定。

		return 0

	#

	#cci折角、所有的顶点
	def cci_dd(self,ccilist):
		cci=ccilist
		dd_li=[]
		#判断折角
		dd_li.append('lx')#第一个cci线为连续
		total=len(cci)
		for i in range(2,total):
			today=i
			lastday=i-1
			yesteday=i-2
			zz=self.__cci_ana_updown(cci[today],cci[lastday],cci[yesteday])
			if zz==1:
				dd_li.append('up')
			elif zz==-1:
				dd_li.append('dw')
			else:
				dd_li.append('lx')
		dd_li.append('lx')#最后一个cci线为连续
		return dd_li
	#cci折角3、去除无用顶点
	def cci_ana_dd(self,ccilist):
		dd_li=self.cci_dd(ccilist)
		#判断相邻连续折角,根据缠论
		up_li=[]
		dw_li=[]
		lxzj_li=[]
		lxzj_li.append(0)
		cci=ccilist
		total=len(cci)
		for i in range(1,total):
			if dd_li[i]=='lx':lxzj_li.append(0)
			elif dd_li[i]!='lx':
				kk=lxzj_li[i-1]+1
				lxzj_li.append(kk)

		#去掉没用的折角
		in_li=[]
		zz_li=[]
		for i in range(total-1,-1,-1):
			
			if lxzj_li[i]==0:continue
			if i in in_li:continue

			#单独的折角
			if lxzj_li[i]==1 :
				zz_li.append(i)

			#连续折角
			if lxzj_li[i]>1 :
				h=lxzj_li[i]
				for p in range(0,h):
					in_li.append(i-p)
				if h==2 or h==4:continue
				
				if h==3:
					#3个角取值
					if dd_li[i]=='up':
						if cci[i]>=cci[i-2]:
						 	zz_li.append(i)
						else:
							zz_li.append(i-2)
					
					if dd_li[i]=='dw':
						if cci[i]<=cci[i-2]:
						 	zz_li.append(i)
						else:
							zz_li.append(i-2)

				if h>3 and h%2==1:
					#或取最大最小值
					if dd_li[i]=='up':zz_li.append(i)
					if dd_li[i]=='dw':zz_li.append(i)

				if h>3 and h%2==0:
					if dd_li[i]=='up':
						zz_li.append(i)
						zz_li.append(i-h-1)
					if dd_li[i]=='dw':
						zz_li.append(i)
						zz_li.append(i-h-1)
		for i in zz_li:
			if dd_li[i]=='up':
				up_li.append(i)
			if dd_li[i]=='dw':
				dw_li.append(i)
		#print(dw_li,up_li)
		in_li.clear()
		lxzj_li.clear()
		dd_li.clear()

		return up_li,dw_li

			#cci折角、所有的顶点

	#选择底折点
	def sel_dd_dw(self,cci):
		total=len(cci)
		cciqr=self.cci_ana_qrfj(cci)
		up_li,dw_li=self.cci_ana_dd(cci)
		
		bz=0
		dw_li2=[]
		for i in range(0,total):
			#强势下不画线
			if cciqr[i]>0:
				bz=0
				continue
			#是折点的
			if i not in dw_li:continue
			#bz为堆栈，选择两个顶点
			#其中一个顶点在100和-100之外
			#压栈
			if  bz==0:bz=i
			if  cci[i]<=cci[bz]:
				bz=i
			elif  cci[i]>cci[bz]:
					dw_li2.append([bz,cci[bz],i,cci[i]])
					bz=0
		up_li.clear()
		dw_li.clear()
		return dw_li2
	#选择顶折点
	def sel_dd_up(self,cci):
		total=len(cci)
		cciqr=self.cci_ana_qrfj(cci)

		up_li,dw_li=self.cci_ana_dd(cci)
		#print(up_li)
		up_li2=[]
		bz=0
		for i in range(0,total):
			#弱势下不画线
			if cciqr[i]<0:
				bz=0
				#print(i)
				continue
			#是顶点的
			if i not in up_li:continue
			#bz为堆栈，选择两个顶点
			#压栈
			if  bz==0:bz=i
			if  cci[i]>=cci[bz]:
				bz=i
			elif  cci[i]<cci[bz]:
						up_li2.append([bz,cci[bz],i,cci[i]])
						bz=0
		return up_li2
	#股价底背离

	#股价底背离
	def gj_di_bl(self,df):
		cci=self.cci
		dw_li2=self.sel_dd_dw(cci)
		#print(dw_li2)
		low_li=df.low.values.tolist()
		dw_li=[]
		for u in dw_li2:
			if low_li[u[0]]>=low_li[u[2]]:
				#print(u)
				dw_li.append(u)
		return dw_li

	#cci 股价顶背驰
	def gj_din_bc(self,df):
		cci=self.cci
		up_li2=self.sel_dd_up(cci)
		#print('Lp1',up_li2)
		high_li=df.high.values.tolist()
		up_li=[]
		for u in up_li2:
			if high_li[u[0]]<=high_li[u[2]]:
				#print(u)
				up_li.append(u)
		return up_li
	#底背驰优化
	def bc(self):

		cci=self.cci
		df=self.df
		cciqr=self.cci_ana_qrfj(cci)
		dw_li=self.gj_di_bl(df)
		up_li=self.gj_din_bc(df)
		ln=len(cci)
		for i in range(ln-1,-1,-1):
			##最后一个是底背离
			if len(dw_li)==0:
				continue
			if i == dw_li[-1][2]:#返回背离点
				return -1,dw_li[-1][0],i
			#最后一个是顶背离
			if len(up_li)==0:
				continue
			if i == up_li[-1][2]:#返回背离点
				return 1,up_li[-1][0],i
		return 0,0,0
	def bc9(self):
		a,b,c=self.bc()
		cn1=a>0#最后一个顶背驰

		if cn1 and (c-b) in [8]:
			return 1
		return 0


#获取数据的接口类
class jiekou:

	#获取基础信息
	def getbasc(self,code1list):
		'''函数--获取基础信息，根据列表['000001','all']'''
		csv_path='d:/stock_csv/{}.csv'.format('basc')
		if 'all' in code1list:print('获取所有Stock')
		jk=file_op()
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
		#返回Stock list
		return st_list

	def getkl(self,code,ktype1):
		'''函数--获取k线'''
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
#策略5----中轨之上连跌3日以上
class boll3(bollorder):
	'''策略5----中轨之上连跌3日以上 bo3'''
	def dueorder(self):
		i=self.boll3()
		#print('boll3',i)
		if i>3:
			return 1
		return 0
		
#策略6----30日红盘占比
class ccibc6(cciorder):
	'''策略6----背驰6 bc6'''
	def dueorder(self):
		a,b,c=self.bc()
		cn1=a>0#最后一个顶背驰

		if cn1 and (c-b) in [6]:
			return 1
		return 0

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

#函数--根据代码获取单个策略
def test101(code1):
	jk=jiekou()
	s=jk.getbasc(code1)[-1]
	print (test101.__doc__,s)
	code1=s.code
	#获取k线记基础指标
	szb=stockzb(s)
	m=m_kl()#月线修饰
	w=w_kl()#周线修饰
	d=D_kl()#日线修饰
	hf=Hf_kl()#30线修饰
	#应用策略
	#1--日线策略
	szb.decorator(d)#日线修饰
	szb.getk()#获取k线
	print(szb.df.columns)

	co=cciorder(szb)
	list_bloc=co.cci_qr_blok()
	print(list_bloc)
	print(szb.df.loc[list_bloc[-1][0]].date)
	print(szb.df.loc[list_bloc[-1][1]].date)

	return 0

def getorderresult(s):
	'''函数--根据代码获取单个策略'''
	#s=getstockbasics(code1)
	print (getorderresult.__doc__,s)
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
	strategy[4] = Context(boll3(szb))
	strategy[5] = Context(ccibc6(szb))
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
	op=file_op()
	dmd_li1=op.get_txt('sv_dmd1.csv').code.values.tolist()
	for code in dmd_li1:
		co=getSixDigitalStockCode(code)
		tt.append(co)

	#tt=['600359','600609','002498',	'002238','300415','000987',	'600598','000931']#tt=['all']
	#tt=['000725']
	st_list=jk.getbasc(tt)#获取符合的代码Stock，，tt=['all']
	#容错
	if len(st_list)==0:
		print('没有符合的代码')
		return 0
	
	
	#获取所有策略结果
	for s in st_list:
		jg_li=getorderresult(s)#获取策略结果
		order_js_list.extend(jg_li)#集合所有结果

	#结果集存入order.csv
	#加入时间节点
	gxrq = datetime.datetime.now().strftime('%Y%m%d')
	gxsj = datetime.datetime.now().strftime('%H%M')
	gx=gxrq+gxsj
	
	
	df=DataFrame(order_js_list,columns=[ 'code', 'name','cl','clname'])
	df['gxsj']=str(gx)
	df.to_csv('order.csv')#为增加方式
	
	return 0
#函数 ---分离策略结果集
def fl_ordercsv():
	'''函数 ---分离策略结果集'''
	op=file_op()
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
	#print(get_all_orderresult.__doc__)
	#get_all_orderresult()
	#print(fl_ordercsv.__doc__)
	#fl_ordercsv()
	test101('002498')
	