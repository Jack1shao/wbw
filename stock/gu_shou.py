#gu_shou.py
from gu_zb import gu_zb
from gu_save import gu_save
import datetime
from pandas import read_csv
from pandas.core.frame import DataFrame
#
class gu_shou(object):
	"""docstring for gu_shou"""
	def __init__(self, arg):
		super(gu_shou, self).__init__()
		self.arg = arg
	#cci向上
	def cci_up(self,code,df):
		#ng_li=[]
		hh=gu_zb('')
		cci=hh.cci(df)
		cciqr=hh.cci_ana_qrfj(cci)
		ln=len(cci)
		if cciqr[ln-1]>0 and cci[ln-1]>cci[ln-2]:
			return  1
		return 0
	#cci折角向上	
	def cci_up_2(self,code,df):
		#ng_li=[]
		hh=gu_zb('')
		cci=hh.cci(df)
		cciqr=hh.cci_ana_qrfj(cci)
		ln=len(cci)
		if cciqr[ln-1]>0 and cci[ln-1]>cci[ln-2] and cci[ln-2]<cci[ln-3]:
			return  1
		cci.clear()
		cciqr.clear()
		return 0

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
		ng_li=df33.code.values.tolist()
		for co2 in ng_li:
			code=self.getSixDigitalStockCode(co2)
			print(code)
			df=kk.get_k_from_db(code,'w')
			if df.empty:
				df=kk.get_k_from_api(code,'w')
				kk.save_to_csv(code,df,'a')
		return 1

def main():
	print('this message is from main function')
	s=gu_shou('')
	#s.m_tiaojian()
	s.w_tiaojian()

if __name__ == '__main__':
	main()
		

