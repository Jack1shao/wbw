#
from getstockClass import getstock
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
				s5,s10=self.find_vol(df,index1)
				#print(s5,s10,int(df.loc[index1,'volume']))
				if int(df.loc[index1,'volume'])>s5 :
					print(s5,s10,int(df.loc[index1,'volume']))
					return i
		return 0
	#计算5日10日交易量
	def find_vol(self,df,index1):
		s5vol=0
		s10vol=0
		for x in range(10):
			s10vol+=df.loc[index1-x-1,'volume']
		for x in range(5):
			s5vol+=df.loc[index1-x-1,'volume']

		return int(s5vol/5),int(s10vol/10)
	#MA=近N日收盘价的累计之和÷N
	#得到一个倒叙的list
	def  MA(self,df,N):
		MA_list=[]
		listindex=[]
		for index,row in df.iterrows():
			listindex.append(index)
		l=listindex[-1]
		#df['ma']=None
		print(df.loc[0,'close'])
		print(df.loc[l,'close'])
		for ind in range(0,l):

			index2=l-ind
			if index2>=N:x=0
			else:x=index2-N
			#print(df.loc[0,'close'])
			#求均值
			lsdf=df[x:index2]['close'].mean()
			#df.ix[index2,'ma']=lsdf
			#print(df.loc[index2,'ma'])
			MA_list.append(lsdf)
		#print(df[0:10])
		print(MA_list[-1])
		return MA_list

	def Md(self,df,N,ma):
		Md_list=[]
		listindex=[]
		for index,row in df.iterrows():
			listindex.append(index)
		#
		#ma=self.MA(df,N)
		l=listindex[-1]
		for ind in range(0,l):

			a=0
			#少于N个 时 ii起作用
			ii=0
			for x in range(N):
				if l-ind-x<=0:break
				ii+=1;
				a+=(ma[ind-x]-df.loc[l-ind-x-1,'close'])
			
			Md_list.append(a/ii)
		print(Md_list[0])
		#print(len(Md_list),Md_list)
		return Md_list
	def TP(self,df,index):
		tp=0
		tp=df.loc[index,'high']+df.loc[index,'low']+df.loc[index,'close']
		#print(df.loc[index,'high'],df.loc[index,'low'],df.loc[index,'close'])
		#print(tp/3)
		return tp/3
	def cci(self,df,index1,N):
		#CCI（N日）=（TP－MA）÷MD÷0.015
		listindex=[]
		for index,row in df.iterrows():
			listindex.append(index)
		#
		#ma=self.MA(df,N)
		l=listindex[-1]
		cci=0
		ma=self.MA(df,N)
		md=self.Md(df,N,ma)
		tp=self.TP(df,index1)
		print(ma[l-index1],md[l-index1],tp)
		cci=(tp-ma[l-index1])/(md[l-index1]*0.015)
		print(cci)
		return cci


	def test2(self):
		df,name=self._getk()
		index=640
		N=14
		print(name,df.loc[index,'date'])
		#(self.cci(df,index,N))
		self.MA(df,N)

	def test(self):
		df,name=self._getk()

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
			if ind>0:
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