#fenxiClass
#股票分析类
from gupiaoClass import gupiaoClass
import mpl_finance as mpf
import matplotlib.pyplot as plt
import talib
class fenxi(gupiaoClass):
	"""docstring for fenxi"""
	
	def cci(self):
		df=self.select_k()
		cci=talib.CCI(df.high,df.low,df.close, timeperiod=14)
		#print(len(cci))
		return cci
	def cci_ana(self,index):
		listcci=self.cci()
		print(len(listcci))
		if index<2:print('The end ');return 0,0,0
		cci=listcci[index]
		refcci1=listcci[index-1]
		refcci2=listcci[index-2]
		return cci,refcci1,refcci2

	def macd(self,df,index):
		macd1,macd2,macd3=talib.MACD(df['close'],fastperiod=12, slowperiod=26, signalperiod=9)
		return macd1,macd2,macd3
	def mcad_ana(self):
		pass
	def  boll(self,df,index):
		up,mid,lo=talib.BBANDS(df.close,timeperiod=20,nbdevup=2,nbdevdn=2,matype=0)
		return up,mid,lo
	def boll_ana():
		pass
	def dmi(self,df,index):
		MINUS_DI=talib.MINUS_DI(df.high,df.low,df.close,timeperiod=14)
		PLUS_DI = talib.PLUS_DI(df.high,df.low,df.close, timeperiod=14)
		ADX = talib.ADX(df.high,df.low,df.close, timeperiod=6)
		ADXR = talib.ADXR(df.high,df.low,df.close, timeperiod=6)
		return MINUS_DI,PLUS_DI,ADX,ADXR
	def dmi_ana(self):
		pass	
	#分析当前k线

	def _fxdq(self,df,index):
		if df.empty and index1<3:
			print("Error:DF is empty or Df is not enof..")
			return 0
		i=index
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
				return -1
		#顶分型
		if low<low1 and low2<low1:
			return 1
		return 0
	#底
	def di(self,df,index):
		i=-1 if self._fxdq(df,index)==-1 else 0

		#加cci分析
		bz_cci=1
		cci,refcci1,refcci2=self.cci_ana(index) 
		if (cci>-100 and refcci1<-100) or (cci>100 and refcci1<100):
			bz_cci=1
		else :bz_cci=0
		return i*bz_cci
	#顶
	def din(self,df,index):
		i=1 if self._fxdq(df,index)==-1 else 0
		return i
	#上涨中继
	def szzj(self,df,index):
		pass 

	def history():
		pass

def  main():
	kk=fenxi('300377')
	df=kk.select_k()
	index=df.index.values[-1]
	print(df[-1:])
	print(kk.cci_ana(640))

	li=[]
	for x in range(index+1):
		i=index-x
		if x<4:li.append(0);continue
		z=kk.di(df,x)
		li.append(z)
	#print(li,len(li))
	X=3
	Y=1
	fig = plt.figure()
	ax1=fig.add_subplot(X,Y,1)
	ax2=fig.add_subplot(X,Y,2)
	ax3=fig.add_subplot(X,Y,3)	

	mpf.candlestick2_ochl(ax=ax1,opens=df["open"].values, closes=df["close"].values, highs=df["high"].values, lows=df["low"].values,width=0.7,colorup='r',colordown='g',alpha=0.7)
	ax2.plot(li)
	ax3.plot(kk.cci())
	plt.show()
	return 0

main()
#h=gupiaoClass('002340').select_k()
#kk=fenxi('002340')
#print(kk.di(kk.select_k()))