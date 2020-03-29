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
	#cci上个周期有背驰
	#cci背驰线被穿越
	#寻找第三波
	#小钝角：之后穿越背驰线，
	#两点画线
	def line(self,x1,y1,x2,y2):
		k=(y2-y1)/(x2-x1)
		b=y2-k*x2
		c1=(300-b)/k
		c2=(-200-b)/k
		return k,b,c1,c2
	def xdj(self,cci1,cci2,cci3):
		print(cci1,cci2,cci3)
		if cci1>cci2 and cci2>cci3:
			x1=1
			y1=cci1
			x2=2
			y2=cci2
			x3=3
			y3=cci3
			k,b,c1,c2=self.line(x1,y1,x2,y2)
			alf1=math.atan(k) * 180 / math.pi
			alf3=math.atan(k3) * 180 / math.pi
			if alf1>-45 and k3>-1:
				print(k,k3)
				return 1
		
		return 0

	#大顶：背驰线之上，股价创新高，cci下折


	def  m_tiaojian(self):
		ng_li=[]
		kk=gu_save('')
		hh=gu_zb('')
		df=kk.get_base_from_api()
		code_li=df.index.values.tolist()
		for co in code_li:
			code=str(co)
			df=kk.get_k_from_db(code,'m')
			if self.cci_up_2(code,df)>0:
				ng_li.append(code)
		ng_lli=[]
		gxrq = datetime.datetime.now().strftime('%Y-%m-%d')
		gxsj = datetime.datetime.now().strftime('%H%M')
		for co2 in ng_li:
			ng_lli.append([co2,'m'])
		df22=DataFrame(ng_lli)
		df22['gxrq']=gxrq
		df22['gxsj']=gxsj
		df22.to_csv('ng.csv',mode='a',header=False)
		
		df33=kk.get_from_csv('ng.csv')
		print(df33)
		return 1
	def getSixDigitalStockCode(self,code):
		strZero = ''
		for i in range(len(str(code)), 6):
			strZero += '0'
		return strZero + str(code)
	def w_tiaojian(self):
		kk=gu_save('')
		df33=kk.get_from_csv('ng.csv')
		#ng_li=df33[].tolist()
		#print(df33.head())
		#df33.columns(['code','ktype','gxrq','gxsj'])
		#print(df33.code.values.tolist())
		ng_li_m=df33.code.values.tolist()
		ng_li_z=[]
		for co2 in ng_li_m:
			code=self.getSixDigitalStockCode(co2)
			print(code)
			df=kk.get_k_from_db(code,'w')
			if df.empty:
				df=kk.get_k_from_api(code,'w')
				kk.save_to_csv(code,df,'a')
				df=kk.get_k_from_db(code,'w')
			if self.cci_up_2(code,df)>0:
				ng_li_z.append(code)
		print(ng_li_z,len(ng_li_z))
		ng_lli=[]
		gxrq = datetime.datetime.now().strftime('%Y-%m-%d')
		gxsj = datetime.datetime.now().strftime('%H%M')
		for co2 in ng_li_z:
			ng_lli.append([co2,'w'])
		df22=DataFrame(ng_lli)
		df22['gxrq']=gxrq
		df22['gxsj']=gxsj
		df22.to_csv('ng_w.csv',mode='a',header=False)

		return 1
	def shou(self,codelist,ktype1):
		pass
	def p_1(self,code1,ktype1):
		kk=gu_save('')
		hh=gu_zb('')
		df=kk.get_k_from_csv(code1,ktype1)
		cci=hh.cci(df)
		c=cci[-4:]
		self.xdj(c[0],c[1],c[2])


def main():
	print('单独执行gu_shou收索，开始')
	s=gu_shou('')
	#s.w_tiaojian()
	s.p_1('600598','w')

if __name__ == '__main__':
	main()
		

