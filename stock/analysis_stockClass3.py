# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:20:38 2020

@author: Administrator
"""
from getstockClass import getstock
from stock_save import stock_saveClass
import talib
import mpl_finance as mpf
import matplotlib.pyplot as plt
import numpy as np
from pandas.core.frame import DataFrame
class analysis_stockClass(object):
	"""docstring for analysis_stockClass"""
	def __init__(self, arg):
		super(analysis_stockClass, self).__init__()
		self.arg = arg
		self.code=arg
		self.total=400
		self.begin=0
		self.end=0

	def _getk(self):
		k=getstock(self.code)
		name=''
		h=stock_saveClass(self.code)
		df=h.stock_from_csv()
		if df.empty:
			h.stock_to_csv()
			df=h.stock_from_csv()
		return df,name
	def get(self,df,rows1):
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

	def macd(self,df,index):
		diff,dea,macd3=talib.MACD(df['close'],fastperiod=12, slowperiod=26, signalperiod=9)
		return diff,dea,macd3

	def boll(self,df):
		up,mid,lo=talib.BBANDS(df.close,timeperiod=20,nbdevup=2,nbdevdn=2,matype=0)
		return up,mid,lo
	def cci(self,df):
		#def CCI(df, n):
		#  PP = (df['high'] + df['low'] + df['close']) / 3
		#CCI = pd.Series((PP - pd.rolling_mean(PP, n)) / pd.rolling_std(PP, n) / 0.015, name = 'CCI' + str(n))
		#return CCI
		cci=talib.CCI(df.high,df.low,df.close, timeperiod=14)
		return cci.tolist()
		#强弱分界点
	def cci_ana_qrfj(self,ccilist):
		
		cci1=ccilist
		bz1=0
		cciqrfj=[]
		for i in range(0, self.total):
			if cci1[i]>100:bz1=1
			if cci1[i]<-100:bz1=-1
			if bz1>0:cciqrfj.append(1)
			else:
				cciqrfj.append(-100)
			
		#print(cci2)
		return cciqrfj
	#cci折角
	def cci_ana_updown(self,c1,c2,c3):
		if c2>c1 and c2>c3:return 1
		if c2<c1 and c2<c3:return -1
		return 0
	#cci折角
	def cci_ana_dd(self,ccilist):
		cci=ccilist
		dd_li=[]
		up_li=[]
		dw_li=[]
		for i in range(2,self.total):
			today=i
			lastday=i-1
			yesteday=i-2
			zz=self.cci_ana_updown(cci[today],cci[lastday],cci[yesteday])
			if zz==1:
				dd_li.append([lastday,cci[lastday],'up'])
			if zz==-1:
				dd_li.append([lastday,cci[lastday],'dw'])
		pass

	#卖点分析
	def maidian(self):
		
		#变量初始化区域
		bz=[]
		#取数据区域
		df1,name=self._getk()
		cci=self.cci(df1)[-self.total:]
		cci_qr=self.cci_ana_qrfj(cci)
		#up,mid,lo=self.boll(df1)
		df=df1[-self.total:]

		high_li=self.get(df,'high')
		low_li=self.get(df,'low')
		open_li=self.get(df,'open')
		close_li=self.get(df,'close')

		#计算数据区域
		#<1>三条线都上涨的卖出条件M1
		#z1=HIGH>BHIGH AND BHIGH>CHIGH AND CLOSE>BCLOSE AND BCLOSE>CCLOSE ;/*三连涨*/
		for i in range(2,self.total):
			today=i
			lastday=i-1
			yesteday=i-2
			tc=cci[today]<cci[yesteday]#cci变小向下
			#三连涨
			t1=high_li[today]>=high_li[lastday] and high_li[lastday]>=high_li[yesteday] \
				and close_li[today]>=close_li[lastday] and close_li[lastday]>=close_li[yesteday]#三连涨
			#新高收阴
			t2=high_li[today]>=high_li[lastday] and high_li[today]>=high_li[yesteday] \
				and close_li[today]<open_li[today]

			if t1 and tc and cci[today]>90:
				bz.append([today,cci[today],'M1'])

			if t2 and tc and cci[today]>90:
				bz.append([today,cci[today],'M2'])
		
		#清理
		close_li.clear()
		open_li.clear()
		high_li.clear()
		low_li.clear()
		#画线区域
		fig = plt.figure()
		X=2
		Y=1
		ax5=fig.add_subplot(X,Y,1)
		ax2=fig.add_subplot(X,Y,2)
		#画K线
		mpf.candlestick2_ochl(ax=ax5,opens=df["open"].values.tolist(), closes=df["close"].values, highs=df["high"].values, lows=df["low"].values,width=0.7,colorup='r',colordown='g',alpha=0.7)
		#画boll
		#ax5.plot(up[-self.total:],'r')
		#ax5.plot(mid[-self.total:],'r')
		#ax5.plot(lo[-self.total:],'r')
		#画cci指标
		ax2.plot(cci,'r')
		ax2.plot(cci_qr,'y')
		#画两点线
		plt.axhline(y=100, color='b', linestyle=':')
		plt.axhline(y=-100, color='b', linestyle=':')

		#叠加文字
		c_text=bz

		for x in c_text:
			plt.text(x[0],x[1],x[2],size = 10)
		
		#print(high_li)
		plt.show()
		return 0

k=analysis_stockClass('600120')

k.maidian()