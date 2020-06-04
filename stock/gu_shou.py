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
		
	#输出字符串，顶底背驰，顶为S，底为B	
	def buy_0(self,df):
		
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
		return 'k'+cu

	#底背驰.返回最后一个背驰
	def d_bc(self,df):
		kk=gu_zb('')
		cci=kk.cci(df)
		cciqr=kk.cci_ana_qrfj(cci)
		dw_li=kk.gj_d_bl(df)
		up_li=kk.gjbc(df)
		ln=len(cci)
		for i in range(ln-1,-1,-1):
			if len(dw_li)==0:
				continue
			if i == dw_li[-1][2]:#返回背离点
				return -1,dw_li[-1][0],i
			if len(up_li)==0:
				continue
			if i == up_li[-1][2]:#返回背离点
				return 1,up_li[-1][0],i
		#底顶点
		#判断背驰
		return 0,0,0

	def shou_bc(self,code1,ktype1):
		kk=gu_save('')
		hh=gu_zb('')
		df=kk.get_k_from_csv(code1,ktype1)
		cci=hh.cci(df)
		return self.bc(cci)
	#最后一个背驰是顶背驰
	def shou_din_bc(self,code1,ktype1):
		#
		kk=gu_save('')
		hh=gu_zb('')
		df=kk.get_k_from_csv(code1,ktype1)
		cci=hh.cci(df)
		pass
	#市值收索
	def shou_sz(self,x1,x2):
		kk=gu_save('')
		code_list=kk.get_code_list()
		c_li=[]
		for code  in code_list:
			sz=kk.get_sz(code)
			if sz>x1 and sz<x2:
				c_li.append([code,'市值在{0}-{1}之间'.format(x1,x2)])

		df=DataFrame(c_li,columns=[ 'code', 'name'])
		df.to_csv('shou.csv')
		return c_li

	#第一次搜，月
	def shou_all_Macd_M_H(self):
		c_li=[]
		kk=gu_save('')
		code_list=kk.get_from_csv('sv_sz.csv').code.values.tolist()
		for code in code_list:
			co=(kk.getSixDigitalStockCode(code))
			print(co)
			f=self.shou_Macd_M_H(co)
			if f==1:
				c_li.append([co,'月线Macd红柱'])
		df=DataFrame(c_li,columns=[ 'code', 'name'])
		df.to_csv('shou_m.csv')
		'''if len(df)>590:
									df1=df[:590]
									df1.to_csv('shou_m1.txt')
									df1=df[591:]
									df1.to_csv('shou_m2.txt')
								else:
									df.to_csv('shou_m1.txt')'''

		c_li.clear()
		return 0
	#第二次搜，周
	def shou_all_Macd_w(self):
		c_li=[]
		kk=gu_save('')
		#周
		code_list=kk.get_from_csv('shou_m.csv').code.values.tolist()
		for code in code_list:
			co=(kk.getSixDigitalStockCode(code))
			print(co)
			f=self.shou_Macd_w_0z(co)
			if f==1:
				c_li.append([co,'周线macd的Dea在0轴之上'])
		df=DataFrame(c_li,columns=[ 'code', 'name'])
		df.to_csv('shou_w.csv')
		if len(df)>590:
			df1=df[:590]
			df1.to_csv('shou_w1.txt')
			df1=df[591:]
			df1.to_csv('shou_w2.txt')
		else:
			df.to_csv('shou_w1.txt')
		c_li.clear()
		return 0
	#
	def shou_all_d(self):
		self.shou_all_Macd_M_H()
		self.shou_all_cci_d()
		self.shou_all_dmi_d()
		return 0
	#第三次搜，日
	def shou_all_cci_d(self):
		kk=gu_save('')
		c_li=[]
		c_li2=[]
		c_li3=[]
		c_li4=[]
		code_list=kk.get_from_csv('shou_m.csv').code.values.tolist()
		for code in code_list:
			co=(kk.getSixDigitalStockCode(code))
			f=self.shou_bc_last_s(co)
			if f==1:
				c_li3.append([co,'最后一个是顶背驰'])
				c_li4.append(co)
		#print(c_li3)
		for code in code_list:

			co=(kk.getSixDigitalStockCode(code))
			#if co in c_li4:
				#continue
			#print(co)
			f=self.shou_cci_D_qrs(co)
			if f==1:
				c_li.append([co,'强势、cci 0+'])
			if f==2:
				c_li2.append([co,'弱势、cci-100-'])
		df=DataFrame(c_li,columns=[ 'code', 'name'])
		df.to_csv('shou_d1_cci.txt')
		df=DataFrame(c_li2,columns=[ 'code', 'name'])
		df.to_csv('shou_d2_cci.txt')

		df=DataFrame(c_li3,columns=[ 'code', 'name'])
		df.to_csv('shou_d3_cci.txt')
		c_li.clear()
		c_li2.clear()
		return 0
	
	#dmi搜，日
	def shou_all_dmi_d(self):
		kk=gu_save('')
		c_li=[]
		c_li2=[]
		c_li3=[]

		gxrq = datetime.datetime.now().strftime('%Y-%m-%d')
		gxsj = datetime.datetime.now().strftime('%H%M')
		code_list=kk.get_from_csv('shou_m.csv').code.values.tolist()
		#计算增加部分
		code_list2=kk.get_from_csv('shou_d1.txt').code.values.tolist()
		c_l=[]
		for code in code_list2:
			co=(kk.getSixDigitalStockCode(code))
			c_l.append(co)

		for code in code_list:
			co=(kk.getSixDigitalStockCode(code))
			f=self.shou_dmi_d(co)
			if f==1:
				c_li.append([co,'趋势增强'+gxrq+gxsj])
				if co not in c_l:
					c_li3.append([co,'新增'+gxrq+gxsj])
			if f==2:
				c_li2.append([co,'趋势减弱'])


		df=DataFrame(c_li,columns=[ 'code', 'name'])
		df.to_csv('shou_d1.txt')
		df=DataFrame(c_li2,columns=[ 'code', 'name'])
		df.to_csv('shou_d2.txt')
		df=DataFrame(c_li3,columns=[ 'code', 'name'])
		df.to_csv('shou_d3.txt',mode='a',header=False)
		return 0

	def shou_dmi_d(self,code1):
		kk=gu_save('')
		hh=gu_zb('')
		df=kk.get_k_from_csv(code1,'D')
		x_dmi=hh.sel_dmi(df)
		return x_dmi


	#搜月Macd为红柱，cci拐头向上。
	def shou_Macd_M_H(self,code1):
		kk=gu_save('')
		hh=gu_zb('')
		df=kk.get_k_from_csv(code1,'m')
		#如果不存在该代码的数据？？？

		#搜月Macd为红柱
		diff,dea,macd3=hh.macd(df)
		macd=macd3.tolist()
		cn1=macd[-1]>0#Macd为红柱

		if cn1 :
			return 1#Macd为红柱
		return 0
	#搜周Macd-dea为在0轴上
	def shou_Macd_w_0z(self,code1):
		kk=gu_save('')
		hh=gu_zb('')
		#搜周Macd-dea为在0轴上
		df=kk.get_k_from_csv(code1,'w')
		diff,dea3,macd3=hh.macd(df)
		dea=dea3.tolist()
		cn2=dea[-1]>0#dea 0轴之上
		if cn2:
			return 1
		return 0

	#搜日线 cci 弱势时 cci<-100;强势时 cci>0
	def shou_cci_D_qrs(self,code1):
		kk=gu_save('')
		hh=gu_zb('')
		df=kk.get_k_from_csv(code1,'D')
		cci=hh.cci(df)
		cciqrfj=hh.cci_ana_qrfj(cci)
		cn4=cciqrfj[-1]>0 and cci[-1]>0
		cn5=cciqrfj[-1]<1 and cci[-1]<-100
		
		if cn4 :
			return 1
		if cn5:
			return 2
		return 0
	#	搜日线最后一个背驰为顶背驰，只有主动背驰，才有主动上涨
	def shou_bc_last_s(self,code1):
		kk=gu_save('')
		hh=gu_zb('')
		df=kk.get_k_from_csv(code1,'D')
		li_last_s=self.buy_0(df)[-1]
		if li_last_s=='s':
			return 1
		return 0

def main():
	print('单独执行gu_shou收索，开始')
	sh=gu_shou('')
	i=0
	while i<10:
		i+=1
	
		print('1--搜 <日K线>')
		print('2--搜 <周K线>周线macd的Dea在0轴之上')
		print('3--搜 <月K线>月线Macd红柱')

		print('99--退出<99>')
		print('--')
		print('--')
		cc=input()
		if cc=='99':
			print('	退出<99>')
			break
		if cc=='3':
			sh.shou_all_Macd_M_H()
			print('---	月线Macd红柱---')
		if cc=='2':
			sh.shou_all_Macd_w()
			print('---	周线macd的Dea在0轴之上---')
		if cc=='1':
			sh.shou_all_d()
			print('---	日K线---')

	print('程序完成，退出')	
	#sh.shou_all_Macd_M_H()
	#sh.shou_all_Macd_w()
	#sh.shou_all_cci_d()
	return 0
if __name__ == '__main__':
	main()
		

