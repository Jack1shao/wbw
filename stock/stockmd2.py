#stockmd.py
#基础
import numpy as np
import os
from pandas import read_csv
from abc import ABCMeta, abstractmethod
from pandas.core.frame import DataFrame
import talib
import tushare as ts
import datetime
from collections import namedtuple
from operClass import file_op
from Tooth_sjjg import queue
#
Stock=namedtuple('Stock','code name hangye totals')
#策略结果
Cljg=namedtuple('Cljg','code name cl jg qz files')

#策略类
class bollorder:
	def __init__(self,stockzb):
		self.stockzb=stockzb
	def boll3(self,start,end):
		'''函数--所有股价在中轨之上'''
		
		df=self.stockzb.df
		close_li=df.close.values.tolist()
		up,mid,lo=self.stockzb.boll()

		mid_li=mid.tolist()
		#在中轨之上
		
		for i in range(start,end+1):
			#跌破中轨
			if close_li[i]<mid_li[i]:
				return 0
		return  1

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
		self.stockzb=stockzb
		self.code =stockzb.stock.code
		self.name =stockzb.stock.name
	def getname(self):
		return self.name
	def getcode(self):
		return self.code
	def getdmi(self):
		PDI,MDI,ADX,ADXR=self.stockzb.dmi()
		return ADX
	#cci折角1、判断
	def __cci_ana_updown(self,c1,c2,c3):
		if c2>c1 and c2>c3:return 1
		if c2<c1 and c2<c3:return -1
		return 0

	#强弱分界点
	def cci_ana_qrfj(self):
		bz1=0
		cciqrfj=[]
		cci1=self.cci
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
		vol=self.df.volume.values.tolist()
		#两个状态值，当两个状态值不一致时，说明状态发生变化。
		bz0=0
		bz1=0
		cciqrfj=[]
		total=len(cci1)
		dd=self.cci_dd(cci1)

		for i in range(0, total):

			if cci1[i]>100:
				bz1=1

			if cci1[i]<-100:
				bz1=-1
			#核对格式为[582, 607, 1, 26, 0.78], [608, 632, -1, 25, 0.22], [633, 639, 1, 7, 0.23]]
			
			if  bz1!=bz0 or i==total-1 :
				if i==total-1:cciqrfj.append(i)#最后一条记录

				start=cciqrfj[0]
				end=cciqrfj[-1]

				#开始取该段的最高价和最低价,日平均交易量
				hi_list=[]#最高价
				lo_list=[]#最低价
				vol_li=[]#交易量
				dd_li=[]#顶点
				for x in range(start,end+1):
					if dd[x]=='up' and cci1[x]>=95:
						dd_li.append(x)		

				for x in range(start,end+1):
					hi_list.append(high1[x])
					lo_list.append(low[x])
					vol_li.append(vol[x])

				#该段最高，最低	
				max1=max(hi_list)
				min1=min(lo_list)
				kj=(max1-min1)/min1#振幅
				#日平均交易量
				jyl_day=np.mean(vol_li)/10000
				#顶点个数
				ddgs=len(dd_li)
				#加入数组
				cci_blok.append([start,end,bz0,len(cciqrfj),float('%.2f'%kj),float('%.1f'%jyl_day),ddgs,dd_li])
				#清空cciqrfj
				cciqrfj=[]
		
			cciqrfj.append(i)
			bz0=bz1
			#块[625, 639, 1, 15, 0.23, 140.6, 2, [627, 631]]
		return cci_blok

	#区块头形态
	def cci_gd(self,start,end):
		'''区块中的高点'''
		gd_li=[]#[xh,cci,gj_high]
		bz0=0
		bz1=0
		cciqk=[]
		for i in range(start,end+1):
			if cci1[i]>100:
				bz1=1
			if cci1[i]<=100:
				bz1=-1
			if bz1!=bz0 or i==end:
				st1=cciqk[0]
				en1=cciqk[-1]
				#顶点个数
				#顶点位置
				#块的宽度
				#
				cciqk=[]

			cciqk.append(i)
			bz0=bz1

		return 0


	#顶点间存在冲顶的形态(小丁与大定)
	def ddzj_chongding(self,dd1,dd2):
		'''顶点间存在冲顶的形态'''
		#顶点是否涨停，与高点的距离，分小丁与大定。
		#dd1，dd2为顶点间
		cci1=self.cci
		high1=self.df.high.values.tolist()
		low1=self.df.low.values.tolist()
		c_li=[]
		h_li=[]
		iii=0#计数器,做为冲顶指数，数字越大，将调整越长。
		bz_c=cci1[dd1]
		bz_hi=high1[dd1]
		for i in range(dd1+1,dd2+1):
			if low1[i]>low1[i-1] and high1[i]<high1[i-1]:continue
			if cci1[i]<bz_c and high1[i]>bz_hi:
				iii+=1
				bz_c=cci1[i]
				bz_hi=high1[i]
			else:
				break
		return iii#计数器,做为冲顶指数，数字越大，将调整越长。

	#顶点间存在背驰
	def ddzj_beichi(self,dd1,dd2):
		''''顶点间存在背驰'''
		cci1=self.cci
		high1=self.df.high.values.tolist()

		iii=0#计数器,做为冲顶指数，数字越大，将调整越长。
		dd1_c=cci1[dd1]
		dd1_hi=high1[dd1]
		dd2_c=cci1[dd2]
		dd2_hi=high1[dd2]
		#高点之间幅度
		fd=(dd2_hi-dd1_hi)/dd1_hi*100
		#背驰的条件
		cn1=dd1_c>dd2_c
		cn2=dd1_hi<dd2_hi
		if cn1 and cn2:
			return 1,dd2-dd1+1,'{}%'.format('%.2f'%fd)
			#返回1,dd2-dd1+1,'{}%'.format('%.2f'%fd)
		#返回[是否背驰，顶点间距离，高点间幅度]
		return 0,dd2-dd1+1,'{}%'.format('%.2f'%fd)#返回[是否背驰，顶点间距离，高点间幅度]
	
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

	def cci_j4(self,dd,end):
	
		'''函数--所有股价在中轨之上'''
		cci1=self.cci
		#if cci[dd]<150:return 0
		
		df=self.df
		close_li=df.close.values.tolist()
		up,mid,lo=self.stockzb.boll()

		mid_li=mid.tolist()
		#在中轨之上
		bz_cci=cci1[dd]
		dd2=dd+3
		if dd+3>end:dd2=end
		for i in range(dd,dd2):
			#跌破中轨
			if cci1[i]>bz_cci:return 0
			if close_li[i]<mid_li[i]:
				return 0
			bz_cci=cci1[i]

		return  1

	##cci dmi 同步折点
	def cci_dmi(self):
		PDI,MDI,ADX,ADXR=self.stockzb.dmi()
		#adx顶点
		dd_li=self.cci_dd(ADX)
		#cci顶点
		dd2_li=self.cci_dd(self.cci)
		#
		l=len(ADX)
		#队列，用于判断同时这点
		q=queue(maxsize=2)
		s_li=[]

		for i in range(0,l):
			ss=[]
			#adx是折点，入队
			if dd_li[i]!='lx':
				#print('dmi',i,ADX[i],dd_li[i],self.df.loc[i].date)
				q.put([dd_li[i],i,self.df.loc[i].date,'dmi',ADX[i]])
				ss=q.get()
				if len(ss)==2:
					if ss[0][0]==ss[1][0]:#收集趋同折点
						ls=[]
						for s in ss:
							for ssss in s:
								ls.append(ssss)
						s_li.append(ls)

			#cci是折点，入队
			if dd2_li[i]!='lx':
				#print('cci',i,self.cci[i],dd2_li[i],self.df.loc[i].date)
				q.put([dd2_li[i],i,self.df.loc[i].date,'cci',self.cci[i]])
				ss=q.get()
				if len(ss)==2:
					if ss[0][0]==ss[1][0]:#收集趋同折点
						ls=[]
						for s in ss:
							for ssss in s:
								ls.append(ssss)
						s_li.append(ls)

		#for x in s_li:
			#if x[0]=='dw':print(x)
		return s_li
	#cci dmi 同步折点之前
	def cci_dmi_q(self):
		'''cci dmi 同步折点之前'''
		#有三种情况，1、同降，2、cci上折，dmi降，3，cci 降，dmi上折
		PDI,MDI,ADX,ADXR=self.stockzb.dmi()
		cci =self.cci
		cciqrfj=self.cci_ana_qrfj()
		#条件
		#1、cci降
		cn1=cci[-1]<cci[-2]
		#2、cci上折
		cn2=cci[-1]>cci[-2] and cci[-3]>cci[-2]
		cn3=cci[-1]>cci[-2] and cci[-3]<cci[-2] and cci[-3]<cci[-4]#2天前

		#3、dmi降
		cn4=ADX[-1]<ADX[-2]
		#4、cci上折
		cn5=ADX[-1]>ADX[-2] and ADX[-3]>ADX[-2]
		cn6=ADX[-1]>ADX[-2] and ADX[-3]<ADX[-2] and ADX[-3]<ADX[-4]#2天前

		#5、adx 小于20
		cn7=ADX[-1]<20
		qz=0
		if cn1 and cn4:qz=1
		if (cn2 or cn3) and cn4 :qz=2
		if (cn5 or cn6)	and cn1 :qz=2
		if cn7 and qz>0:qz=5
		if qz>0 and cciqrfj[-1]>0:
			qz=5+qz
			return qz
		else:
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
#日@2
class D_kl2(Finery):
	def getk(self,code1):
		Finery.getk(self,code1)
		g=jiekou()
		df=g.get_k_from_api(code1,'D')#实时数据
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
#策略1
class cl1_rsmd(cciorder):
	'''策略1 处于弱势区域 rs'''
	def dueorder(self):
		#总的区域快
		cl,jg,files=self.__doc__.split()
		qz=0
		list_block=self.cci_qr_blok()
		#最后一个区域快
		#print(list_block)
		block_last=list_block[-1]
		#print(block_last)
		#处在弱势区域
		#Cljg=namedtuple('Cljg','code name cl jg qz files')
		if block_last[2]<1:
			qz=1
		else:
			qz=0

		#处在强势区域，第一个顶点cci<150 顶点个数小于3个
		'''if block_last[6] and block_last[6]<=3:
									dd_li=block_last[7]
									dd1=dd_li[0]
									if self.cci[dd1]<150:
										return 2,'''''

		return Cljg(code=self.getcode(),name=self.getname(),cl=cl,jg=jg,qz=qz,files=files)

#策略2
class cl2_cci_cd(cciorder):
	'''策略2 本块中有冲顶 cd'''
	def dueorder(self):
		cl,jg,files=self.__doc__.split()
		#总的区域快
		list_block=self.cci_qr_blok()
		#最后一个区域快
		block_last=list_block[-1]

		if block_last[2]<1:
			return Cljg(code=self.getcode(),name=self.getname(),cl=cl,jg=jg,qz=0,files=files)
		#本块最后一条k线
		lastk_xh=block_last[1]
		#本块的顶点列表
		dd_li=block_last[7]
		l=len(dd_li)#顶点个数
		b=l-2 if l-2>0 else 0#取最后两顶点，判断是否冲顶
		iii=0#冲顶指数
		for i in range(l-1,b-1,-1):
			dd1=dd_li[i]
			dd2=lastk_xh
			iii+=self.ddzj_chongding(dd1,dd2)

		'''策略2 本块中有冲顶 cd'''
		cl,jg,files=self.__doc__.split()
		qz=iii
		return Cljg(code=self.getcode(),name=self.getname(),cl=cl,jg=jg,qz=qz,files=files)
#策略3
class cl_3_b3_j4(cciorder):
	'''策略3 主升浪一型 zs '''
	def dueorder(self):
		cl,jg,files=self.__doc__.split()

		#总的区域快
		list_block=self.cci_qr_blok()
		#最后一个区域快
		block_last=list_block[-1]

		if block_last[2]<1:

			return Cljg(code=self.getcode(),name=self.getname(),cl=cl,jg=jg,qz=0,files=files)
		#本块最后一条k线
		lastk_xh=block_last[1]
		end=lastk_xh
		#本块的顶点列表
		dd_li=block_last[7]
		l=len(dd_li)#顶点个数
		b=l-2 if l-2>0 else 0#取最后两顶点，判断是否冲顶
		iii=0#冲顶指数
		for i in range(l-1,b-1,-1):
			dd1=dd_li[i]
			
			iii+=self.cci_j4(dd1,end)
	
		qz=iii
		return Cljg(code=self.getcode(),name=self.getname(),cl=cl,jg=jg,qz=qz,files=files)
		
		

#策略3----macd红柱
class macdyxhz(macdorder):
	'''策略3----macd红柱 yhz'''
	def dueorder(self):
		macd=self.macd3()
		if macd>0:
			return 1
		return 0
#策略4----dmi横盘或高于80
class cl4_ccianddmi(cciorder):
	'''策略4 cci&dmi趋同折点为买卖点 bs'''
	def dueorder(self):
		cl,jg,files=self.__doc__.split()

		qt_li=self.cci_dmi()
		last=qt_li[-1]
		#趋同点的日期
		l1=len(self.cci)-1
		l2=last[6]
		l=l1-l2
		
		cciqrfj=self.cci_ana_qrfj()

		if last[0]=='dw' and l<4:
			if cciqrfj[-l]>0:
				qz=l
			else:
				qz=10
			
			jg1='{0} 买点在 {1} {2} 天前'.format(jg,last[7],l)
		else:
			qz=0
			jg1='{0} 卖点在 {1} {2} 天前'.format(jg,last[7],l)
		return Cljg(code=self.getcode(),name=self.getname(),cl=cl,jg=jg1,qz=qz,files=files+str(qz))

class cl5_maidianqian(cciorder):
	'''策略5 趋同折点买前 bsq'''
	def dueorder(self):
		cl,jg,files=self.__doc__.split()

		qz=self.cci_dmi_q()
		return Cljg(code=self.getcode(),name=self.getname(),cl=cl,jg=jg,qz=qz,files=files+str(qz))

#策略5----

#策略6----
#策略7----

#管理策略的类
class Context:
	'''管理策略的类'''
	def __init__(self,csuper):
		self.csuper = csuper
	def GetResult(self):
		return self.csuper.dueorder()
#注入策略,返回结果
def yycl(szb):
	'''注入策略'''
	strategy={}
	#注入策略
	strategy[1] = Context(cl1_rsmd(szb))
	strategy[2] = Context(cl2_cci_cd(szb))
	strategy[3] = Context(cl_3_b3_j4(szb))
	strategy[4] = Context(cl4_ccianddmi(szb))
	#strategy[5] = Context(cl5_maidianqian(szb))

	code_order=[]

	for i in range(1,len(strategy)+1):
		x=strategy[i].GetResult()
		#策略结果说明 去除不符合的结果， qz=0
		if x.qz>0:code_order.append([x.code,x.name,x.cl,x.jg,x.qz,x.files])
	return code_order

#股票代码补齐
def getSixDigitalStockCode(code):
		strZero = ''
		for i in range(len(str(code)), 6):
			strZero += '0'
		return strZero + str(code)

#测试函数--根据代码获取单个策略
def test101(code1):

	jk=jiekou()
	s=jk.getbasc(code1)[-1]
	#获取k线记基础指标
	szb=stockzb(s)
	d=D_kl2()#日线修饰,实时数据
	hf=Hf_kl()#30线修饰
	#应用策略
	#1--日线策略
	szb.decorator(d)#日线修饰
	szb.getk()#获取k线

	#注入策略
	res=yycl(szb)

	

	#详细分析
	co=cciorder(szb)
	list_bloc=co.cci_qr_blok()
	

	b=co.cci_dmi()
	l=len(b)
	dmi=co.getdmi()
	iii=0
	for bloc in list_bloc[-3:]:
		iii+=1
		print(' ******** 第{}区域块 *******'.format(iii),bloc)
		start=bloc[0]
		end=bloc[1]
		print('=====up===')
		for x in b:
			print(x[7]) if x[6]>=start and x[6]<=end and x[0]=='up' else 0	
		print('=====dw===')	
		for x in b:
			print(x) if x[6]>=start and x[6]<=end and x[0]=='dw' else 0
			
		#[print(x,b[x]) for x in range(len(b)-20,len(b)) if b[x][0]=='up' and b[x][6]>=bloc[0] and b[x][6]<=bloc[1]]
		#[print('cci=%.2f'%co.cci[b[x][6]],'dmi=%.2f'%dmi[b[x][6]],b[x]) for x in range(0,len(b)) if (b[x][0]=='dw' and b[x][6]>=bloc[0] and b[x][6]<=bloc[1])]

	print('\n',s)
	print('最后一个k线',list_bloc[-1][1],szb.df.loc[list_bloc[-1][1]].date)
	[print(re) for re in res]

	#[print('cci=%.2f'%co.cci[b[x][6]],'dmi=%.2f'%co.getdmi()[b[x][6]],b[x]) for x in range(len(b)-30,len(b)) if b[x][0]=='dw']
	return 0
#函数--根据代码获取单个策略
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

	#---------应用策略--------
	#1--日线策略
	szb.decorator(d)#日线修饰
	szb.getk()#获取k线
	#执行应用策略
	code_order=yycl(szb)
	
	#return code_order#临时屏蔽月线月线策略
	#2--月线策略
	#szb.decorator(m)#月线修饰
	#szb.getk()#获取月线
	#执行应用策略
	#code_order=yycl(szb)
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
	#tt=['300216','002238','300415','000987',	'600598','000931']
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
	
	columns_li=[ 'code', 'name','cl','cljg','qz','files']
	if len(order_js_list)>0:
		if len(order_js_list[-1])!=len(columns_li):
			print("数据列数量不等")
		df=DataFrame(order_js_list,columns=columns_li)
		df['gxsj']=str(gx)
		df.to_csv('order.csv')#为增加方式

	return 0
#函数--获取给点集合代码所有策略

#函数 ---分离策略结果集
def fl_ordercsv():
	'''函数 ---分离策略结果集'''
	op=file_op()
	cl_df=op.get_txt('order.csv')
	#分类文件名去重
	fil=list(set(cl_df.files.values.tolist()))
	print(fil)

	for na in fil:
		files1=na+'.txt'
		df=cl_df[cl_df.files==na]
		#print(na,files1)
		#print(df.head())
		df.to_csv(files1)
	return 0

def main():
	print('\n---策略主程序---')

	i=0
	while i<10:
		i+=1
		print('执行策略分析---1')
		print('分离结果集---2')
		print('单代码分析---6位代码')
		print('99--退出<99>')
	
		cc=input()
		if cc=='99':
			print('	退出<99>')
			break
		ccc=int(str(cc))
		if ccc<=0 and ccc>=10:
			print('代码错误')
			continue
		if ccc==1:
			print(get_all_orderresult.__doc__)
			get_all_orderresult()
		if ccc==2:
			#分离结果集
			print(fl_ordercsv.__doc__)
			fl_ordercsv()

		if len(cc)==6:
			test101(str(cc))


	return 0

if __name__ == '__main__':
	#输入股票代码获取该代码的基础信息
	#l=getorderresult('000931')
	#print(get_all_orderresult.__doc__)
	#get_all_orderresult()
	#print(fl_ordercsv.__doc__)
	#fl_ordercsv()
	test101('002444')
	main()
	#test101('000333')
	