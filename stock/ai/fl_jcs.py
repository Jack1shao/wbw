import sys,os
print(sys.path)
sys.path.append('d:/py/wbw/stock/')
from  stockmd2 import jiekou
from sklearn import datasets
import pandas as pd
#import mglearn
from operClass import file_op
class dataset_gu():
	'''用于学习的数据'''
	def __init__(self):
		self.file1='d:/gupiao/aiyb2020.csv'

	def save_date(self):
		'''用于学习的数据2'''
		print(self.__doc__)
		tt=[]
		jk=jiekou()
		#大名单列表存入tt
		op=file_op()
		dmd_li1=op.get_txt_line('../sv_dmd1.csv')
		#dmd_li1=op.get_txt_line('sv_dmd1.csv').code.values.tolist()
		return 0
		for code in dmd_li1:
			co=getSixDigitalStockCode(code)
			tt.append(co)
		tt=['002498','600359','600609']
		st_list=jk.getbasc(tt)#获取符合的代码Stock，，tt=['all']
		iii=0
		#str_pcci=(co.p_cci).__doc__
		#print(str_pcci)
		#return 0
		for s in  st_list:
			iii+=1
			#获取k线记基础指标
			szb=stockzb(s)
			d=D_kl()#日线修饰,实时数据
			#应用策略
			szb.decorator(d)#日线修饰
			szb.getk()#获取k线

			#详细分析
			co=cciorder(szb)
			b=co.cci_dmi()
			md1=[]
			for x in b:
				
				if x[0]=='dw' and x[3]=='cci':
					
					md1.append(x[1])
				if x[0]=='dw' and x[8]=='cci':
				
					md1.append(x[6])
			code2=co.getcode()
			name=co.getname()
			#md1=[]
			yb_li=[]
			yb_li30=[]
			for xh in md1:
				
				l_cci=co.p_cci(xh)
				l_adx=co.p_adx(xh)
				l_vol=co.p_vol(xh)
				l_macd=co.p_macd(xh)
				l_boll=co.p_boll(xh)
				l_gj=co.p_gj(xh)
				l_tj=co.tj(xh)
				date_xh=co.df.loc[xh].date
				tjlb=0
				if l_tj[2]<=0:
					tjlb=-1
				elif l_tj[2]>0 and l_tj[2]<10:
					tjlb=1
				elif l_tj[2]>=10 and l_tj[2]<20:
					tjlb=2
				elif l_tj[2]>=20:
					tjlb=3
				else:
					tjlb=0
		
				yb_li30.append([code2,date_xh]+l_cci[1:]+l_adx[1:]+l_macd[1:]+l_boll[1:]+l_vol+l_gj+[tjlb])
				#elif l_tj[1]>10 or l_tj[2]>10 and l_tj[3]>0:
					#print(l_tj)
					#yb_li.append([code2,date_xh]+l_cci+l_adx+l_macd+l_boll+l_vol+l_gj+l_tj)
				#print(l_cci+l_adx+l_macd+l_boll+l_vol+l_gj+l_tj)
			#print(iii,len(yb_li),yb_li30)
			#df=DataFrame(yb_li)
			#df.to_csv('d:/aiyb10.csv',mode='a',header=False,encoding='utf-8')
			gxrq = datetime.datetime.now().strftime('%Y-%m-%d')
			files1='d:/aiyb{}.csv'.format(gxrq)
			df2=DataFrame(yb_li30)
			df2.to_csv(files1,mode='a',header=False,encoding='utf-8')

		return 0

	def get_date(self):
		file1=self.file1
		fo=file_op()
		df=fo.get_from_csv(file1)
		#df=''
		return df

class jlmx():

	def xlmx():
		'''训练模型'''
		return

	def savemx():
		'''保存模型'''
		return 0

	def getmx():
		'''调用模型'''
		return 0
		
		
d=dataset_gu()
d.save_date()
#df=d.get_date()

#y=df.columns[-2:]
#print(df[y].head())
