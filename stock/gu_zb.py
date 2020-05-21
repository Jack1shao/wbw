#gu_zb.py
import talib

class gu_zb(object):
	"""docstring for gu_zb"""
	def __init__(self, arg):
		super(gu_zb, self).__init__()
		self.arg = arg

	def macd(self,df):
		diff,dea,macd3=talib.MACD(df['close'],fastperiod=12, slowperiod=26, signalperiod=9)
		return diff,dea,macd3
	#指标boll
	def boll(self,df):
		up,mid,lo=talib.BBANDS(df.close,timeperiod=20,nbdevup=2,nbdevdn=2,matype=0)
		return up,mid,lo
	#指标ma
	def ma(self,df):
		closed=df['close'].values
		sma=talib.MA(closed,timeperiod=34,matype=0)
		return sma.tolist()
	#指标cci
	def cci(self,df):
		#def CCI(df, n):
		#  PP = (df['high'] + df['low'] + df['close']) / 3
		#CCI = pd.Series((PP - pd.rolling_mean(PP, n)) / pd.rolling_std(PP, n) / 0.015, name = 'CCI' + str(n))
		#return CCI
		cci=talib.CCI(df.high,df.low,df.close, timeperiod=14)
		return cci.tolist()
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
	#强弱势区域
	def cci_qsqy(self,cci1):
		qsqy=[]
		rsqy=[]
		qs=[]
		rs=[]
		
		qr=self.cci_ana_qrfj(cci1)
		ln=len(qr)
		for i in range(0,ln):
			if qr[i]>0:
				qsqy.append(i)
			if qr[i]<0 and len(qsqy)>0:
				qs.append([qsqy[0],qsqy[-1]])
				qsqy.clear()
			if qr[i]<0:
				rsqy.append(i)
			if qr[i]>0 and len(rsqy)>0:
				rs.append([rsqy[0],rsqy[-1]])
				rsqy.clear()	
		if len(qsqy)>0:
			qs.append([qsqy[0],qsqy[-1]])
		if len(rsqy)>0:
			rs.append([rsqy[0],rsqy[-1]])
		#print(qs[-4:])
		return qs,rs
	#判断区域大级别背驰。
	def cci_qy_dd(self,cci1,list_qy):
		if len(list_qy)!=2:
			print('error 1001010')
			return 0
		start=list_qy[0]
		end=list_qy[-1]
		all_dd=self.cci_dd(cci1)

		d1=[]
		d2=[]
		for i in range(start,end):
			if all_dd[i]=='up':
				d1.append(i)
		ln=len(d1)
		if ln <2:
			return []
		if ln==2:
			return [d1[0],cci[d1[0]],d1[1],cci[d1[1]]]
		
		#判段第一个点是否顶	
		zz=self.__cci_ana_updown(100,cci[d1[0]],cci[d1[1]])
		if zz==1:
			d2.append(d1[0])

		#中间有顶
		for x in rang(2,ln):
			if ln<3:
				break
			today=d1[x]
			lastday=d1[x-1]
			yesteday=d1[x-2]
			zz=self.__cci_ana_updown(cci[today],cci[lastday],cci[yesteday])
			if zz==1:
				d2.append(d1[x-1])
		#判段最后一个点是否顶		
		zz=self.__cci_ana_updown(cci[d1[-2]],cci[d1[-1]],-100)
		if zz==1:
			d2.append(d1[-1])
		if len(d2)>1:
			return d2
		else:
			return []
	#cci折角1、判断
	def __cci_ana_updown(self,c1,c2,c3):
		if c2>c1 and c2>c3:return 1
		if c2<c1 and c2<c3:return -1
		return 0
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

	def cci_ana_dd2(self,ccilist):
		cci=ccilist
		dd_li=[]
		up_li=[]
		dw_li=[]
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
		#for i in range(0,total):
			#print(i,dd_li[i],cci[i])
		#判断相邻连续折角,根据缠论
		lxzj_li=[]
		lxzj_li.append(0)
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
				if h==2 or h==4 or h==6:continue
			
				if h==3 or h==5 or h==7:
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
		for i in zz_li:
			if dd_li[i]=='up':
				up_li.append(i)
			if dd_li[i]=='dw':
				dw_li.append(i)
	
		in_li.clear()
		lxzj_li.clear()
		dd_li.clear()

		return up_li,dw_li
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
	#股价底背离
	def gj_bl(self,df):
		up_li=[]
		dw_li=[]
		low_li=df.low.values.tolist()
		high_li=df.high.values.tolist()

		cci=self.cci(df)
		cciqr=self.cci_ana_qrfj(cci)
		dd_li=self.cci_dd(cci)
		total=len(cci)
		for i in range(0,total):
			if dd_li[i]=='up':
				up_li.append(i)
			if dd_li[i]=='dw':
				dw_li.append(i)
		#底顶点背驰		
		dw_li2=[]
		up_li2=[]
		bz=0
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
				if low_li[i]<low_li[bz]:
					dw_li2.append([bz,cci[bz],i,cci[i]])
				bz=0
		#顶顶点背驰
		bz=0
		for i in range(0,total):
			#弱势下不画线
			if cciqr[i]<0:
				bz=0
				continue
			if i not in up_li:continue#是顶点的
			#bz为堆栈，选择两个顶点，其中一个顶点在100和-100之外
			if  bz==0:bz=i#压栈
			if  cci[i]>=cci[bz]:
				bz=i
			elif  cci[i]<cci[bz]:
				if high_li[i]>high_li[bz]:
						up_li2.append([bz,cci[bz],i,cci[i]])
				bz=0

		return up_li2,dw_li2
		
	#股价底背离
	def gj_d_bl(self,df):
		cci=self.cci(df)
		dw_li2=self.sel_dd_dw(cci)
		#print(dw_li2)
		low_li=df.low.values.tolist()
		dw_li=[]
		for u in dw_li2:
			if low_li[u[0]]>=low_li[u[2]]:
				#print(u)
				dw_li.append(u)
		return dw_li

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
	#cci 股价同时背驰
	def gjbc(self,df):
		cci=self.cci(df)
		up_li2=self.sel_dd_up(cci)
		print('Lp1',up_li2)
		high_li=df.high.values.tolist()
		up_li=[]
		for u in up_li2:
			if high_li[u[0]]<=high_li[u[2]]:
				#print(u)
				up_li.append(u)
		return up_li
	#底背驰优化