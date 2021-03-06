#
from getstockClass import getstock
from stock_save import stock_saveClass
import talib
import mpl_finance as mpf
import matplotlib.pyplot as plt
import numpy as np
class analysis_stock(object):
	"""docstring for analysis_stock
		分析单只股票k线数据
		月，周，日， 30
	"""
	def __init__(self, arg):
		super(analysis_stock, self).__init__()
		self.arg = arg
		self.code = str(arg)
		self.total=30
		self.begin=0
		self.end=0

	def _getk1(self):
		k=getstock(self.code)
		df=k.GET_KLINE(self.code,'D','2019-05-04','2019-05-04')
		name=k.GET_BASE()
		print("获取--{0}--".format(name))
        
		return df,name

	def _getk(self):
		k=getstock(self.code)
		name=k.GET_BASE()
		h=stock_saveClass(self.code)
		df=h.stock_from_csv()
		if df.empty:
			h.stock_to_csv()
			df=h.stock_from_csv()
		return df,name

	def get(self,rows1):
		colum=['open','high','close','low','volume']
		list_r=[]
		if rows1 not in colum:return [],0
		df,name=self._getk()


		list_r=df[rows1].values.tolist()
		ll=len(list_r)
		if ll<1:return [],0
		if self.total>ll:return list_r[-self.total:]
		else:
			return list_r

	#强弱分界点
	def cci_ana_qrfj(self,ccilist):
		total=self.total
		cci1=ccilist.tolist()[-total:]
		bz1=0
		cci2=[]
		for i in range(0, total):
			if cci1[i]>100:bz1=1
			if cci1[i]<-100:bz1=-1
			if bz1>0:cci2.append(100)
			else:
				cci2.append(-100)
			
		#print(cci2)
		return cci2

	def cci(self,df):
		#def CCI(df, n):
		#  PP = (df['high'] + df['low'] + df['close']) / 3
		#CCI = pd.Series((PP - pd.rolling_mean(PP, n)) / pd.rolling_std(PP, n) / 0.015, name = 'CCI' + str(n))
		#return CCI
		cci=talib.CCI(df.high,df.low,df.close, timeperiod=14)
		return cci

	def macd(self,df,index):
		diff,dea,macd3=talib.MACD(df['close'],fastperiod=12, slowperiod=26, signalperiod=9)
		return diff,dea,macd3

	def boll(self,df,index):
		up,mid,lo=talib.BBANDS(df.close,timeperiod=20,nbdevup=2,nbdevdn=2,matype=0)
		return up,mid,lo
	def draw(self,listccc,df):
		fig = plt.figure()
		X=3
		Y=1
		
		ax5=fig.add_subplot(X,Y,1)
		ax2=fig.add_subplot(X,Y,2)
		#画K线
		mpf.candlestick2_ochl(ax=ax5,opens=df["open"].values.tolist(), closes=df["close"].values, highs=df["high"].values, lows=df["low"].values,width=0.7,colorup='r',colordown='g',alpha=0.7)
		#画指标叠加
		for l in listccc:
			ax2.plot(l)
		plt.show()
		return 0
	def cci_ana_updown(self,c1,c2,c3):
		if c2>c1 and c2>c3:return 1
		if c2<c1 and c2<c3:return -1
		return 0
	def drow_line(self,k,b,):
		return
	#cci处理
	def cci_cl(self,df):
		cci1=self.cci(df)
		cci_qrfj=self.cci_ana_qrfj(cci1)#强弱分界点
		cci_ht=cci1.tolist()[-self.total:]#画cci线用的数据
		return cci_ht,cci_qrfj[-self.total:]
	#
	def cci_draw_line(self,cci_ht,cci_qrfj):
		up_li=[]
		dw_li=[]
		for i in range(2,self.total):

			if self.cci_ana_updown(cci_ht[i],cci_ht[i-1],cci_ht[i-2])==1:
				up_li.append([i-1,cci_ht[i-1]])
			if self.cci_ana_updown(cci_ht[i],cci_ht[i-1],cci_ht[i-2])==-1:
				dw_li.append([i-1,cci_ht[i-1]])
		#print(up_li)
		up_li2=[]
		dw_li2=[]
		cci_bz_l=0
		u=1
		for u in range(1,len(up_li)):
			if up_li[u][1]<up_li[u-1][1]:
				i=up_li[u-1][0]
				c1=up_li[u-1][1]
				up_li2.append([i,c1,up_li[u][0],up_li[u][1]])
				break


		return up_li2,dw_li2
	def test3(self):
		df1,name=self._getk()
		
		#cci处理
		cci_ht,cci_qrfj=self.cci_cl(df1)	

		df=df1[-self.total:]	

		#顶点坐标
		up_li2,dw_li2=self.cci_draw_line(cci_ht,cci_qrfj)
		print(up_li2)
		#return 0
		fig = plt.figure()
		X=2
		Y=1
		ax5=fig.add_subplot(X,Y,1)
		ax2=fig.add_subplot(X,Y,2)
		#画K线
		mpf.candlestick2_ochl(ax=ax5,opens=df["open"].values.tolist(), closes=df["close"].values, highs=df["high"].values, lows=df["low"].values,width=0.7,colorup='r',colordown='g',alpha=0.7)
		#画cci指标
		ax2.plot(cci_ht,'r')
		#叠加文字
		#c_text=[]
		'''for i in range(3,self.total):
									if cci_ht[i]<cci_ht[i-1] and cci_ht[i-1]>cci_ht[i-2] and cci_ht[i]>90:
										c_text.append([i,cci_ht[i],'p'])
								for x in c_text:
									plt.text(x[0],x[1],x[2],size = 5,bbox = dict(facecolor = "r", alpha = 0.2))
								'''
		iii=self.total-1
		while cci_qrfj[iii]==100:
			iii-=1
		
		x=np.linspace(0,self.total,10)
		print(up_li2)
		for u in up_li2[-4:]:
			y1=u[1]
			y2=u[3]
			x1=u[0]
			x2=u[2]
			k=(y2-y1)/(x2-x1)
			if k>0:continue
			b=y2-k*x2
			y=k*x+b
			plt.plot(x,y,'-.y')
		#画两点线
		plt.axhline(y=100, color='b', linestyle=':')
		plt.axhline(y=-100, color='b', linestyle=':')
		plt.show()
		
		return 0
	def test2(self):
		df1,name=self._getk()
		index=619
		N=14
		df=df1
		#图表格式
		X=3
		Y=1
		fig = plt.figure()
		ax5=fig.add_subplot(X,Y,1)
		ax2=fig.add_subplot(X,Y,2)
		ax3=fig.add_subplot(X,Y,3)		
		

		print(name,df.loc[index,'date'])

		'''fig = plt.figure()
								ax1=fig.add_subplot(5,1,1)
								ax2=fig.add_subplot(5,1,2)
								ax3=fig.add_subplot(5,1,3)
								ax4=fig.add_subplot(5,1,4)
								ax5=fig.add_subplot(5,1,5)

								ax1.plot(macd1.values.tolist(),'g',macd2.values.tolist(),'b',macd3.values.tolist(),'y')
								ax2.plot(up.values.tolist(),'g',mid.values.tolist(),'b',lo.values.tolist(),'y')
								ax3.plot(cci.values.tolist(),'r')'''

			

		#dmi图
		MINUS_DI,PLUS_DI,ADX,ADXR=self.dmi(df,index)
		l=len(ADX.values.tolist())
		print(l)
		zz=[1 if ADX.loc[x]<MINUS_DI.loc[x] and ADX.loc[x]<PLUS_DI.loc[x]  else 0 for x in range(l)]
		print(zz)
		ax3.plot(zz)
		ax3.plot(PLUS_DI.values.tolist(),'y',MINUS_DI.values.tolist(),'k')
		#ax2.plot(ADX.values.tolist(),'g',ADXR.values.tolist(),'b',PLUS_DI.values.tolist(),'y',MINUS_DI.values.tolist(),'k')
		
		#股价图
		mpf.candlestick2_ochl(ax=ax5,opens=df["open"].values, closes=df["close"].values, highs=df["high"].values, lows=df["low"].values,width=0.7,colorup='r',colordown='g',alpha=0.7)

		plt.show()

	#k线分型
	#分析当前k线上涨1、2或下跌-1，-2


k=analysis_stock('300313')
k.test3()