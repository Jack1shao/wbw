#
from getstockClass import getstock
import talib
import mpl_finance as mpf
import matplotlib.pyplot as plt
class analysis_stock(object):
	"""docstring for analysis_stock
		分析单只股票k线数据
		月，周，日， 30
	"""
	def __init__(self, arg):
		super(analysis_stock, self).__init__()
		self.arg = arg
		self.code = str(arg)

	def _getk(self):
		k=getstock(self.code)
		df=k.GET_KLINE(self.code,'D','2019-05-04','2019-05-04')
		name=k.GET_BASE()
		return df,name
	#寻找分型
	def find_fenxin(self,df,index1):
		#容错
		if df.empty and index1<3:
			print("Error:DF is empty or Df is not enof..")
			return 0
		i=index1
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

		#底分型
		if high>high1 and high2>high1 :
			#必须是阳线
			if close>close1:
				return i
		return 0
	#计算5日10日交易量
	def find_vol(self,df,index1):
		s5=df[index1-5:index1]['volume'].mean()
		s10=df[index1-10:index1]['volume'].mean()
		return s5,s10
	def vol_ana(self,df,index):
		#s5,s10=self.find_vol(df,index)
		#s51,s101=self.find_vol(df,index-1)
		#if s101>s10 :return 0
		if int(df.loc[index,'volume'])<int(df.loc[index-1,'volume']):return 0
		return 1
	def cci_ana(self,df,index):

		pass
	def dmi_ana(self,df,index):

		MINUS_DI=talib.MINUS_DI(df.high,df.low,df.close,timeperiod=14)
		#DX = talib.DX(df.high,df.low,df.close,timeperiod=14)
		PLUS_DI = talib.PLUS_DI(df.high,df.low,df.close, timeperiod=14)
		#PLUS_DM = talib.PLUS_DM(df.high,df.low, timeperiod=14)
		ADX = talib.ADX(df.high,df.low,df.close, timeperiod=6)
		ADXR = talib.ADXR(df.high,df.low,df.close, timeperiod=6)
		adxlist=ADX.values.tolist()
		#plt.plot(ADX.values.tolist(),'g',ADXR.values.tolist(),'b',PLUS_DI.values.tolist(),'y',MINUS_DI.values.tolist(),'k'
		#plt.show()
		#if adxlist[index]<adxlist[index-2]:return 0
		if adxlist[index]<25:return 0
		return 1
	def dmi(self,df,index):
		MINUS_DI=talib.MINUS_DI(df.high,df.low,df.close,timeperiod=14)
		#DX = talib.DX(df.high,df.low,df.close,timeperiod=14)
		PLUS_DI = talib.PLUS_DI(df.high,df.low,df.close, timeperiod=14)
		#PLUS_DM = talib.PLUS_DM(df.high,df.low, timeperiod=14)
		ADX = talib.ADX(df.high,df.low,df.close, timeperiod=6)
		ADXR = talib.ADXR(df.high,df.low,df.close, timeperiod=6)
		return MINUS_DI,PLUS_DI,ADX,ADXR

	def cci(self,df,index):
		cci=talib.CCI(df.high,df.low,df.close, timeperiod=14)
		return cci
	def macd(self,df,index):
		macd1,macd2,macd3=talib.MACD(df['close'],fastperiod=12, slowperiod=26, signalperiod=9)
		return macd1,macd2,macd3

	def  boll(self,df,index):
		up,mid,lo=talib.BBANDS(df.close,timeperiod=20,nbdevup=2,nbdevdn=2,matype=0)
		return up,mid,lo
		

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
		ax2.plot(PLUS_DI.values.tolist(),'y',MINUS_DI.values.tolist(),'k')
		#ax2.plot(ADX.values.tolist(),'g',ADXR.values.tolist(),'b',PLUS_DI.values.tolist(),'y',MINUS_DI.values.tolist(),'k')
		
		#股价图
		mpf.candlestick2_ochl(ax=ax5,opens=df["open"].values, closes=df["close"].values, highs=df["high"].values, lows=df["low"].values,width=0.7,colorup='r',colordown='g',alpha=0.7)

		plt.show()



	def test(self):
		df,name=self._getk()
		print(name)
		if df.empty :
			print("Error:DF is empty ..")
			return 0
		listindex=[]
		for index,row in df.iterrows():
			listindex.append(index)
			#print(row['date'],df.loc[index,])
		l=listindex[-1]
		for x in range(l):
			if l-x<30:
				break
			ind=self.find_fenxin(df,l-x)
			if ind>0:
				in_vol=self.vol_ana(df,l-x)
				in_dmi=self.dmi_ana(df,l-x)
				if in_vol*in_dmi==0:
					continue
					

				#if ind>0 and in_vol*in_dmi:
				print(ind,df.loc[ind,'date'],in_vol,in_dmi)
			#else:print(df.loc[l-x,'date'],in_vol,in_dmi)
		index=510
		#N=14
		MINUS_DI,PLUS_DI,ADX,ADXR=self.dmi(df,index)
		
		print(name,df.loc[index,'date'],PLUS_DI.loc[index],MINUS_DI.loc[index],ADX.loc[index],ADXR.loc[index])
		#print(ADX.loc[index],ADX.loc[index-1])

			

	#k线分型
	#分析当前k线上涨1、2或下跌-1，-2
	def k_fenxing(self,df):
		#容错
		if df.empty:
			print("Error:DF is empty..")
			return 0
		listindex=[]
		for index1,row in df.iterrows():
			listindex.append(index1)
			#print(row[])
		i=listindex[-1]
		#容错
		if i<=2:
			print("数据量不够")
			return 0
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

		print(open0,close,high,low)
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
		# print('up=%d,down=%d'%(up,down),open2,close2)
		if (close1>close2 and up==1):return 2 #上涨
		if(open2>=close2 and open2>=close1 and up==1):return 1 #上涨分型
		if open2>close2 and down==1:return -2 #下跌
		if (open2<close2 and down==1):return -1 #分型下跌
		print(up,down)
		return 0

		

	def k_jyl(self,df):
		pass


#

k=analysis_stock('000062')
k.test2()