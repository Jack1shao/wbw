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

	#从后向前第几个强势周期
	def qszq(self,cciqr,x):
		ln=len(cciqr)
		zhq_li=[]
	
		r_li=[]
		#print(cciqr)
		for i in range(0,ln):
			#if cciqr[i]<0:continue
			if cciqr[i]>0:
				zhq_li.append(i)
			if i>1 and cciqr[i-1]>0 and cciqr[i]<0:
				l=len(zhq_li)
				i1=zhq_li[0]
				i2=zhq_li[l-1]
				r_li.append([i1,i2,l])
				#print([i1,i2,ln])
				zhq_li=[]
		print(r_li[-x:])
		return r_li[-x:]
	#cci上个周期有背驰
	def bc(self,cci):
		kk=gu_zb('')
		cciqr=kk.cci_ana_qrfj(cci)
		up_li2,line_li=kk.draw_dd_up(cci)
		#print(up_li2)
		r_li=self.qszq(cciqr,2)
		ln=len(cciqr)
		x1=0
		x2=0
		if cciqr[ln-1]>1:
			x1=r_li[0][0]
			x2=r_li[0][1]
			cont=r_li[0][2]
		else:
			x1=r_li[1][0]
			x2=r_li[1][1]
			cont=r_li[1][2]
		bz=''
		print(x1,x2)
		for u in up_li2:
			if u[0]<x2 and u[0]>x1:
				if x2==ln+1:
					bz='本周期存在背驰'
					print('本周期存在背驰')
				else:
					bz='上周期存在背驰'
					print('上周期存在背驰')
				return 1,bz
		return 0,bz
	
	#cci背驰线被穿越
	#寻找第三波：当前阶段为强势阶段并有背驰，然后等待第三波。
	
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
		df=kk.get_k_from_csv(code1,ktype1)
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
	def shou_sz(self,x1,x2):
		kk=gu_save('')
		code_list=kk.get_code_list()
		c_li=[]
		for code  in code_list:
			sz=kk.get_sz(code)
			if sz>x1 and sz<x2:
				c_li.append([code,'市值在{0}-{1}之间'.format(x1,x2)])
				#break
		#print(len(c_li))
		df=DataFrame(c_li,columns=[ 'code', 'name'])
		df.to_csv('shou.csv')
		return c_li
	#
def main():
	print('单独执行gu_shou收索，开始')
	s=gu_shou('')
	#s.w_tiaojian()
	#s.shou_xdj('600596','D')
	#s.shou_bc('600598','D')
	#code_list=s.shou_sz(100,2000)
	c_li=[]
	kk=gu_save('')
	code_list=kk.get_from_csv('shou.csv').code.values.tolist()
	print(len(code_list))
	for code in code_list:
		co=(kk.getSixDigitalStockCode(code))
		f,bz=s.shou_bc(co,'D')
		if f==1:
			c_li.append([co,bz])
	df=DataFrame(c_li,columns=[ 'code', 'name'])
	df.to_csv('shou2.csv')

	#if s.get_timeToMarket('600598')>20191231:print('dddddd')

if __name__ == '__main__':
	main()
		

