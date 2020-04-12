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
	def bc(self,df):
		kk=gu_zb('')
		cci=kk.cci(df)
		cciqr=kk.cci_ana_qrfj(cci)
		up_li2=kk.gjbc(df)

		r_li=self.qszq(cciqr,2)
		#print(len(r_li))
		if len(r_li)<2:
			return 0,''
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
		#背驰个数
		bcgs=0
		for u in up_li2:
			if u[0]<x2 and u[0]>x1:
				bcgs+=1
		if x2==ln-1:
			bz='本周期存在背驰'
			print('本周期存在背驰')
		else:
			bz='上周期存在背驰'
			print('上周期存在背驰')
		return bcgs,bz
		
	#买点1、2次底背驰后的大幅调整。（顶底背驰交错出现是什么情况）
	def buy_1(self,df):
		#连续2次底背驰
		pass
	#买点2、cci第一次顶背驰线后，准备穿越。（穿越前会形成同级别的底背驰吗，均线之上会更好些）
	def buy2(self,df):
		#一次顶背驰
		pass
	#买点3、cci第2次顶背驰线后，准备穿越。寻找第三波：当前阶段为强势阶段并有背驰？？，然后等待第三波。
			#
	def buy_3(self,df):
		#连续两次顶背驰
		a=1
		ii=0
		cu=''
		while a!=0 and ii<10 :
			
			a,b,c=self.d_bc(df)
			if a<0:
				cu='b'+cu
				ii+=1
			if a>0:
				cu='s'+cu
				ii+=1
			if a!=0:
				df=df[:b]
		print(cu)
		if cu.find('ssbb')>0:
			print('buy_3')
		return cu

	#中枢
	#def 
	#底背驰.返回最后一个背驰
	def d_bc(self,df):
		kk=gu_zb('')
		cci=kk.cci(df)
		cciqr=kk.cci_ana_qrfj(cci)
		dw_li=kk.gj_d_bl(df)
		up_li=kk.gjbc(df)
		ln=len(cci)
		for i in range(ln-1,-1,-1):
			if i == dw_li[-1][2]:#返回背离点
				return -1,dw_li[-1][0],i
			if i == up_li[-1][2]:#返回背离点
				return 1,up_li[-1][0],i
		#底顶点
		#判断背驰
		return 0,0,0
	#搜索2根小阴线，在100之上，每天2个点之内，高点都在boll上轨之上
	def two_little(self,code,ktype1):
		kk=gu_save('')
		hh=gu_zb('')
		df=kk.get_k_from_csv(code,ktype1)
		cci=hh.cci(df)
		up,mid,lo=hh.boll(df)
		#print(up.tolist())
		high_li=df.high.values.tolist()
		open_li=df.open.values.tolist()
		close_li=df.close.values.tolist()
		ln=len(cci)
		ttt_li=[]
		for i in range(2,ln):
			cn1=cci[i]>100 and cci[i-1]>100 and cci[i]<cci[i-1]
			cn2=high_li[i]>up[i] and high_li[i-1]>up[i-1]
			cn3=open_li[i]>close_li[i] and open_li[i-1]>close_li[i-1] 
			cn4=open_li[i-2]<close_li[i-2] and close_li[i]<close_li[i-1] and  close_li[i-1]<close_li[i-2] 
			if cn1 and cn2 and cn3 and cn4:
				print(code,i,df.loc[i].date)
				ttt_li.append([code,i,df.loc[i].date])

		return len(ttt_li),ttt_li
	#标记大顶：背驰线之上，股价创新高，cci下折
	def jddd(self,df):
		high_li=df.high.values.tolist()
		close_li=df.close.values.tolist()
		open_li=df.open.values.tolist()
		kk=gu_zb('')
		cci=kk.cci(df)
		ln=len(cci)
		jddd_li=[]
		for i in range(2,ln):
			cn1=high_li[i-2]<high_li[i-1] and high_li[i-1]<high_li[i]
			cn2=close_li[i]>close_li[i-1] and close[i-1]>close_li[i-2]
			cn3=close_li[i]>open_li[i] and close_li[i-1]>open_li[i-1] and close_li[i-2]>open_li[i-2]
			if cn1 and cn2 and cn3:
				jddd_li.append([i,'大顶'])
		open_li.clear()
		close_li.clear()
		high_li.clear()
		return jddd_li



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
	#小钝角
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
	#市值收索
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
	#底背离
	def dbl(self,df):
		hh=gu_zb('')
		low_li=df.low.values.tolist()
		diff,dea,macd3=hh.macd(df)
		return 1


	def test(self):
		kk=gu_save('')
		hh=gu_zb('')
		df=kk.get_k_from_csv('002498','D')
		#cci=hh.cci(df)
		#cciqr=hh.cci_ana_qrfj(cci)
		#zq=self.qszq(cciqr,2)
		dd=self.d_bc(df)
		print(dd)
		return 0

	def shou_tt_all(self):
		c_li=[]
		kk=gu_save('')
		code_list=kk.get_from_csv('shou.csv').code.values.tolist()
		for co in code_list:
			code=(kk.getSixDigitalStockCode(co))
			f,ttt_li=self.two_little(code,'D')
			if f:
				print(ttt_li)
		return 0

	def shou_bc_all(self):
		c_li=[]
		kk=gu_save('')
		code_list=kk.get_from_csv('shou.csv').code.values.tolist()
		#周
		code_list=[]
		for code in code_list:
			co=(kk.getSixDigitalStockCode(code))
			f,bz=s.shou_bc(co,'w')
			if f==1:
				c_li.append([co,bz])
		df=DataFrame(c_li,columns=[ 'code', 'name'])
		df.to_csv('shou_w.csv')
		#首日先 
		code_list=kk.get_from_csv('shou_w.csv').code.values.tolist()
		#code_list=[]
		for code in code_list:
			co=(kk.getSixDigitalStockCode(code))
			f,bz=s.shou_bc(co,'D')
			if f==1:
				c_li.append([co,bz])
		df=DataFrame(c_li,columns=[ 'code', 'name'])
		df.to_csv('shou_d.csv')
		c_li.clear()
		return 0
	#搜索底背驰
	def shou_dibc_all(self):

		return 0
def main():
	print('单独执行gu_shou收索，开始')
	s=gu_shou('')
	#s.w_tiaojian()
	#s.shou_xdj('600596','D')
	#s.shou_bc('600598','D')
	#code_list=s.shou_sz(100,2000)
	#s.shou_bc_all()
	#s.shou_tt_all()

if __name__ == '__main__':
	main()
		

