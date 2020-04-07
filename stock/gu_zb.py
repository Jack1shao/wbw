#gu_zb.py
import talib
import mpl_finance as mpf
import matplotlib.pyplot as plt
import numpy as np
class gu_zb(object):
	"""docstring for gu_zb"""
	def __init__(self, arg):
		super(gu_zb, self).__init__()
		self.arg = arg

	def macd(self,df):
		diff,dea,macd3=talib.MACD(df['close'],fastperiod=12, slowperiod=26, signalperiod=9)
		return 2
	#指标boll
	def boll(self,df):
		up,mid,lo=talib.BBANDS(df.close,timeperiod=20,nbdevup=2,nbdevdn=2,matype=0)
		return up,mid,lo
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
		js_dw=0
		for i in range(0, total):
			if cci1[i]>100:
				bz1=1
			if cci1[i]<-100:
				bz1=-1
			if bz1>0:
				#去除偶然性
				if i>3:
					cn1=cciqrfj[i-2]<0
					cn2=cci1[i]<100 and cci1[i-1]>100 and cci1[i-2]<100
					if cn1 and cn2:
						bz=-1
						cciqrfj.pop()
						cciqrfj.append(-100)
						cciqrfj.append(-100)
						continue
				cciqrfj.append(js_up)
			else:
				#去除偶然性
				if i>3:	
					cn3=cciqrfj[i-2]>0
					cn4=cci1[i]>-100 and cci1[i-1]<-100 and cci1[i-2]>-100
					if cn3 and cn4:
						bz=1
						cciqrfj.pop()
						cciqrfj.append(js_up)
						cciqrfj.append(js_up)
						continue
				cciqrfj.append(-100)
		return cciqrfj

	#cci折角
	def __cci_ana_updown(self,c1,c2,c3):
		if c2>c1 and c2>c3:return 1
		if c2<c1 and c2<c3:return -1
		return 0
	#cci折角
	def cci_ana_dd(self,ccilist):
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
		#for i in range(0,total):
			#print(i,lxzj_li[i])
		#print(lxzj_li)
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

	#两点画线
	def line(self,x1,y1,x2,y2):
		k=(y2-y1)/(x2-x1)
		b=y2-k*x2
		c1=(300-b)/k
		c2=(-200-b)/k
		return k,b,c1,c2
	#cci折角2
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
		#for i in range(0,total):
			#print(i,lxzj_li[i])
		#print(lxzj_li)
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
			
				if h==3 or h==5:
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
		#print(dw_li,up_li)
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
	def gj_d_bl(self,df):
		cci=self.cci(df)
		dw_li2=self.sel_dd_dw(cci)
		low_li=df.low.values.tolist()
		dw_li=[]
		for u in dw_li2:
			if low_li[u[0]]>=low_li[u[2]]:
				print(u)
				dw_li.append(u)
		return dw_li

	#选择顶折点	
	def sel_dd_up(self,cci):
		total=len(cci)
		cciqr=self.cci_ana_qrfj(cci)
		up_li,dw_li=self.cci_ana_dd(cci)
		#print(up_li)
		#zjd_li=[]
		up_li2=[]
		#line_li=[]
		bz=0
		#print(len(cciqr))
		for i in range(0,total):
			#弱势下不画线
			if cciqr[i]<0:
				bz=0
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
		high_li=df.high.values.tolist()
		up_li=[]
		for u in up_li2:
			if high_li[u[0]]<=high_li[u[2]]:
				#print(u)
				up_li.append(u)
		return up_li