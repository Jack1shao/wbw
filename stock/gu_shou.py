#gu_shou.py
from gu_zb import gu_zb
from gu_save import gu_save
import datetime
from pandas import read_csv
from pandas.core.frame import DataFrame
import math
#
class gu_shou(object):
	"""docstring for gu_shou"""
	def __init__(self, arg):
		super(gu_shou, self).__init__()
		self.arg = arg
	#补全代码	
	def getSixDigitalStockCode(self,code):
		strZero = ''
		for i in range(len(str(code)), 6):
			strZero += '0'
		return strZero + str(code)
	#cci连续向上
	def cci_up_lx(self,cci):
		c=cci[-3:]
		if c[0]<c[1] and c[1]<c[2]:
			return 1
		return 0
	#cci折角向上
	def cci_up_zj(self,cci):
		c=cci[-3:]
		if c[0]>c[1] and c[1]<c[2]:
			return 1
		return 0

	#cci连续向下
	def cci_dw_lx(self,cci):
		c=cci[-3:]
		if c[0]>c[1] and c[1]>c[2]:
			return 1
		return 0
	#cci折角向下
	def cci_dw_zj(self,cci):
		c=cci[-3:]
		if c[0]<c[1] and c[1]>c[2]:
			return 1
		return 0
	#从后向前第几个强势周期
	def qszq(self,cciqr,x):
		ln=len(cciqr)
		q,i1,i2=0
		zhq_li=[]
		s=0
		r_li=[]
		for i in range(0,ln):
			if cciqr[i]<0:continue
			if cciqr[i]>0:
				zhq_li.append(i)
			if i>1 and cciqr[i-1]>0 and cciqr[i]<0:
				ln=len(zhq_li)
				i1=zhq_li[0]
				i2=zhq_li[ln-1]
				r_li.append([i1,i2,ln])
				del zhq_li[:]
		print(r_li)
		return r_li[-x:]
	#cci上个周期有背驰
	def bc(self,cci):
		kk=gu_zb('')
		cciqr=kk.cci_ana_qrfj(cci)
		up_li2,line_li=kk.draw_dd_up(cci)
		#print(up_li2)
		l_qr=len(cciqr)
		qd=0
		ii=0
	
		for i in range(l_qr-1,-1,-1):
			if cciqr[i]==1:
				qd=1
			if qd==1 and cciqr[i]<0:
				ii=i
				break


		for u in up_li2:
			if u[0]<ii:continue
			else:
				print(u)
				return 1
		return 0
		#print(i)
	#cci背驰线被穿越
	#寻找第三波
	#大顶：背驰线之上，股价创新高，cci下折

	#小钝角：之后穿越背驰线，
		#两点画线
	def line(self,x1,y1,x2,y2):
		k=(y2-y1)/(x2-x1)
		b=y2-k*x2
		c1=(300-b)/k
		c2=(-200-b)/k
		return k,b,c1,c2
		#小钝角
	def xdj(self,cci1,cci2,cci3):
		#print(cci1,cci2,cci3)
		if cci1>cci2 and cci2>cci3:
			x1=1
			y1=cci1
			x2=2
			y2=cci2
			x3=3
			y3=cci3
			k,b,c1,c2=self.line(x1,y1,x2,y2)
			k3,b3,c13,c23=self.line(x3,y3,x2,y2)
			alf1=(math.atan(k) * 180 / math.pi)
			alf3=(math.atan(k3) * 180 / math.pi)

			if alf1<0 and alf3<0 and alf3-alf1>10:
				#print(alf1,alf3)
				return 1
		return 0

	def shou_bc(self,code1,ktype1):
		kk=gu_save('')
		hh=gu_zb('')
		df=kk.get_k_from_api(code1,ktype1)
		cci=hh.cci(df)
		return self.bc(cci)

	def shou_xdj(self,code1,ktype1):
		kk=gu_save('')
		hh=gu_zb('')
		df=kk.get_k_from_csv(code1,ktype1)
		#print(df.head())
		day=df.date.values.tolist()
		cci=hh.cci(df)
		up_li,dw_li=hh.cci_ana_dd(cci)
		#cci=cci[-10:]
		d_ln=len(day)
		ln=len(cci)
		#print(d_ln,ln)
		for i in range(2,ln):
			if (i-2) in up_li:continue
			xdj=self.xdj(cci[i-2],cci[i-1],cci[i])
			if i+4>=ln:
				pp=ln-1
			else:pp=i+3
			if xdj==1:
				print(i,day[i],cci[i],df.loc[i]['high'],df.loc[pp]['high'])
		return 0


def main():
	print('单独执行gu_shou收索，开始')
	s=gu_shou('')
	#s.w_tiaojian()
	#s.shou_xdj('600596','D')
	#s.shou('600598','w')

if __name__ == '__main__':
	main()
		

