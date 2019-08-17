#
from getstockClass import getstock
import talib
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
		s5,s10=self.find_vol(df,index)
		s51,s101=self.find_vol(df,index-1)
		if s101>s10 :return 0
		if int(df.loc[index,'volume'])<int(df.loc[index-1,'volume']):return 0
		return 1

	def test2(self):
		df,name=self._getk()
		index=617
		N=14

		print(name,df.loc[index,'date'])
<<<<<<< HEAD
		#real=talib.CCI(df.high,df.low,df.close, timeperiod=14)
		#real=talib.MACD(df['close'],fastperiod=12, slowperiod=26, signalperiod=9)
		#real=talib.BBANDS(df.close,timeperiod=20,nbdevup=1,nbdevdn=1,matype=0)
		up,mid,lo=talib.BBANDS(df.close,timeperiod=20,nbdevup=2,nbdevdn=2,matype=0)
		print(up)
		#self.cci(df,index,N)
		#self.Md(df,N)
		#self.find_vol(df,index)
=======
		#real=talib.CCI(df.high,df.low,df.close)
		#MINUS_DM=talib.MINUS_DM(df.high,df.low,timeperiod=14)
		MINUS_DI=talib.MINUS_DI(df.high,df.low,df.close,timeperiod=14)
		#DX = talib.DX(df.high,df.low,df.close,timeperiod=14)
		PLUS_DI = talib.PLUS_DI(df.high,df.low,df.close, timeperiod=14)
		#PLUS_DM = talib.PLUS_DM(df.high,df.low, timeperiod=14)

		ADX = talib.ADX(df.high,df.low,df.close, timeperiod=14)
		ADXR = talib.ADXR(df.high,df.low,df.close, timeperiod=14)
		#ADXR = talib.DMI(df.high,df.low,df.close, timeperiod=14)
		print(ADX.loc[index],ADXR.loc[index],PLUS_DI.loc[index])
		#print(talib.function())

>>>>>>> 96bd6199642e26504dbed0383b42e0f25b224dde

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
			if l-x<11:break
			ind=self.find_fenxin(df,l-x)
			in_vol=self.vol_ana(df,l-x)
			if ind>0 and in_vol:
				print(ind,df.loc[ind,'date'])
			

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

k=analysis_stock('002340')
k.test2()