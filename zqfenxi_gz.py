#zqfenxi_gz.py
from collections import Counter
from pandas.core.frame import DataFrame
import numpy as np
class zqfenxi_gz(object):
	"""docstring for zqfenxi_gz"""

	#统计数量
	def count(self,list_1):
		li=Counter(list_1)#字典对象
		#li={'0': 3766, '1': 3302, '3': 2955, '2': 2821}
		list_key=[]
		for key in li.keys():
			list_key.append(key)
		#增加没有的数据
		list_columns=[3,2,1,0]
		for key in list_columns:
			if key in list_key:continue
			li.setdefault(key, 0)
		#print(li)	
		list_sg=[]
		list_sg.append(li[3])
		list_sg.append(li[2])
		list_sg.append(li[1])
		list_sg.append(li[0])
		list_sg2=[]
		list_sg2.append(list_sg)
		df=DataFrame(list_sg2,columns=['sg3','sg2','sg1','sg0'])
		return df

	#计算离散值
	def lisan(self,list_1):
		jz=(np.mean(list_1))
		sc=(np.var(list_1))
		bzc=(np.std(list_1))
		lsxs=float('%.4f'%(bzc/jz))
		#print(lsxs,sc)
		return lsxs,float('%.1f'%(sc))

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
	def sg_as(self,sg):
		if sg==0:
			return  ("1")
		elif sg<0:
			return ("0")
		elif sg==1:
	
			return ('2')
		else :
			return ('3')
		return '-1'

	#必发_概率——模型
	def bifa_gl(self,gl3,gl1,gl0):
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
	def bifa_ykzs(self,yk3,yk1,yk0):
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
			
		