class macdorder:
	"""docstring for macdorder"""
	def __init__(self,stockzb):

		self.stockzb=stockzb
	
	def macd3(self):
		diff,dea,macd3=self.stockzb.macd()
		macd=macd3.tolist()
		return macd[-1]

		

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

