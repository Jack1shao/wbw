#zqfenxi.py
from pandas.core.frame import DataFrame
from tooth_excle import tooth_excleClass
from collections import Counter
from zqconfigClass import zqconfigClass
class zqfenxi(object):
	"""docstring for zqfenxi"""
	def __init__(self, arg):
		super(zqfenxi, self).__init__()
		self.arg = arg
		self.idnm=int(arg)
	#赔付率--凯利模型
	def _moxin_hf(self,ck3,ck1,ck0,hf):
		mx=1000
		if ck3*100>=hf:
			mx+=100
		if ck1*100>=hf:
			mx+=10
		if ck0*100>=hf:
			mx+=1
		#是否大于返还率
		#(1111)
		return mx


	#赔付率--凯利模型
	def _moxin_kaili_as(self,ck3,ck1,ck0):
		mx=0
		zz=0

		if ck3>=ck1 and ck3>=ck0:
			if ck3>=1:
				zz=1
			if ck1>=ck0:
				mx=31
			else : 
				mx= (32)
		elif ck1>=ck3 and ck1>=ck0:
			if ck1>=1:
				zz=1
			if ck3>=ck0:
				mx= (11)
			else:
				mx= (12)
		else:
			if ck0>=1:
				zz=1
			if ck3>=ck1:
				mx= (101)
			else:
				mx= (102)
		return mx,zz

	#赔付率-
	def  moxin_kaili(self,df,idnm):
		df1=df[df.idnm==idnm]
		li=[]
		for index,x in df1.iterrows():
			li1=[]
			li1.append(x.idnm)
			li1.append(x.bcgs)
			mx,zz=self._moxin_kaili_as(x.ck3,x.ck1,x.ck0)
			li1.append(mx)
			li1.append(zz)
			hf1=self._moxin_hf(x.ck3,x.ck1,x.ck0,x.chf)
			li1.append(hf1)

			mx1,zz1=self._moxin_kaili_as(x.jk3,x.jk1,x.jk0)
			li1.append(mx1)
			li1.append(zz1)
			hf2=self._moxin_hf(x.jk3,x.jk1,x.jk0,x.jhf)
			li1.append(hf2)

			li1.append('凯利模型')
			li.append(li1)
		#print('凯利模型',li)

		return li
	#赛果_模型
	def  _sg_as(self,sg):


		if sg==0:
			return  ("1")
		elif sg<0:
			return ("0")
		elif sg==1:
			
			return ('2')
		else :
			return ('3')

		return '-1'
	#赛果
	def sg(self,df,idnm):
		df1=df[df.idnm==idnm]
		li=[]
		for index,x in df1.iterrows():
			if len(li)>0:break
			li1=[]
			li1.append(x.idnm)
			li1.append(self._sg_as(x.zjq-x.kjq))
			li1.append('赛果')
			#
			li.append(li1)
		return li
	#必发_概率——模型
	def _bifa_gl(self,gl3,gl1,gl0):
		#20为相差不大，10为相差大
		mx=10
		if abs(gl3)<15 and abs(gl1)<15 and abs(gl0)<15:
			mx=20
		if gl3<=gl1 and gl3<=gl0:
			mx+=3
		elif gl1<=gl3 and gl1<=gl0:
			mx+=1
		else:
			mx+=0
		return mx

	#必发_盈亏指数——模型
	def _bifa_ykzs(self,yk3,yk1,yk0):
		mx=101010
		if yk1<=0:
			mx+=100000
		if abs(yk1)>=20 and abs(yk1)<=30:
			mx+=20000
		if abs(yk1)>30:
			mx+=30000
		if yk3<=0:
			mx+=1000
		if abs(yk3)>=20 and abs(yk3)<=30:
			mx+=200
		if abs(yk3)>30:
			mx+=300
		if yk0<=0:
			mx+=10
		if abs(yk0)>=20 and abs(yk0)<=30:
			mx+=2
		if abs(yk0)>30:
			mx+=3
		return mx
			
	#必发
	def bifa(self,df,idnm):
		df1=df[df.idnm==idnm]
		li=[]
		for index,x in df1.iterrows():
			if len(li)>0:break
			li1=[]
			li1.append(x.idnm)
			mx_gl=self._bifa_gl(x.glc3,x.glc1,x.glc0)
			li1.append(mx_gl)

			mx_yk=self._bifa_ykzs(x.ykzs3,x.ykzs1,x.ykzs0)
			li1.append(mx_yk)
			li1.append('必发模型')
			#
			li.append(li1)
		return li


	#亚盘_交叉盘
	def _yapan_jcp(self,idnm):

		return 0


	#亚盘
	def yapan(self,df,idnm):

		pass


	#已有数据分析
	def fenxi(self):
		df=tooth_excleClass('e:/0.5.xlsx').read()
		#按列值分组
		#df1=df[df.bcgs=='Iceland']
		#df1=df1[df1.idnm==779599]
		list_idnm=df.idnm.values
		id1_list=[]
		for x in list_idnm:
			if x not in id1_list:
				id1_list.append(x)
		fx_list=[]
		iii=0
		for idnm in id1_list:
			iii+=1

			#if iii>10:break
			li=[]
			#序号
			li.append(iii)

			#赛果
			list_sg=(self.sg(df,idnm))
			for x in list_sg:
				li.extend(x)
			#必发
			list_bifa=(self.bifa(df,idnm))
			for x in list_bifa:
				li.extend(x)
			#亚盘
			list_yp=self.yapan(df,idnm)

			#欧赔
			list_oz=self.moxin_kaili(df,idnm)
			list_kong=['',0,0,0,0,0,0]
			list11=[]
			for x in range(5):
				list11.append(list_kong)
			z=-1
			for x in list_oz:
				del x[0]
				x.pop(-1)
				if x[0]=='Iceland':	z=0
				if x[0]=='Oddset':	z=1
				if x[0]=='Expekt':	z=2
				if x[0]=='Sweden':	z=3
				if x[0]=='BINGOAL':	z=4
				if z!=-1:
					del list11[z]
					list11.insert(z,x)

			for x in list11:
				li.extend(x)

			#print(li)
			fx_list.append(li)
		n=len(fx_list[0])
		columns1=[]
		for x in range(n):
			columns1.append('n'+str(x))
		#print(columns1)
		df=DataFrame(fx_list,columns=columns1)
		df.to_csv('e:/555.csv')
		#print(fx_list)
		return df
	def fenxi2(self):
		#df=self.fenxi()
		df=zqconfigClass(0).select('e:/555.csv')
		#DataFrame.columns.values.tolist()
		lm_list=df.columns.values.tolist()
		#print(lm_list)
		#li_not=[0,1,3,4,7,8,15,22,29,36]
		#li_in1=[5,9,11,16,18,23,25,30,32,37,39]
		#li_in2=
		#for x in lm_list:
			#if x in li_not:continue
			#aa=df[x]
			#print(x,set(aa))

		#BINGOAL 
		#N37=31 AND N5=21
		#df1=df[(df.n37==31)&(df.n5==21)]
		#df1=df[(df.n5==21)&df.n37.isin([31,32,11,12,0])]
		#n30 in [31,32] and n37 in [31,32] and n16 in [11,12]
		#n9==11 and n37=11
		#n9==12 and n37=12
		#n37=102 and n30=102 and n23=102 and n5=13
		df1=df[(df.n5>=20)&(df.n23.isin([11,12]))&(df.n37.isin([11,12]))]
		listsg=df1.n2.values
		print(Counter(listsg))

		df1=df[(df.n16.isin([11,12]))&(df.n37.isin([31,32]))&(df.n30.isin([31,32]))]
		listsg=df1.n2.values
		print(Counter(listsg))
		

		return 0


h=zqfenxi('1')
#h.fenxi()
h.fenxi2()
