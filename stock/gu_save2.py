'''获取数据'''
import tushare as ts
import datetime
import os
from pandas import read_csv
from pandas.core.frame import DataFrame
from collections import namedtuple

#
Stock=namedtuple('Stock','code name hangye totals')
ts.set_token('4d4e8c66f3fe804a585a345419362a9982790682a79ef65214b5d5e1')
#数据获取接口
class gu_getfromapi:
	'''从api获取数据'''
	#获取api 数据
	def get_D_k(self,code1,start_d):
		
		'''新的接口Pro'''
		pro = ts.pro_api()
		#日期处理
		rq_now = datetime.datetime.now().strftime('%Y%m%d')
		rq_kaishi='20140103'
		start_d=rq_kaishi if start_d=='' else rq_now
		#获取数据
		df=pro.daily(ts_code=code1, start_date=rq_kaishi, end_date=rq_now)
		df.rename(columns={'vol':'volume','trade_date':'date','ts_code':'code'}, inplace=True) 
		df=df.sort_values(by='date' , ascending=True)
		return df

	#全天模式
	def get_allday_k(self,date):
		ff
		return df
	#获取基础数据api
	def get_base(self):
		df = ts.get_stock_basics()
		rq_now = datetime.datetime.now().strftime('%Y%m%d')
		df['gxrq']=rq_now

		return df

class gu_getfromdb(object):
	"""获取本地数据"""
		
	#获取本地数据
	#获取基础数据db
	def get_base(self):
		basc='basc'
		files1=self.get_csvmc(basc)
		if os.path.exists(files1):
			with open(files1,'r',encoding='utf-8') as csv_file:
				df = read_csv(csv_file,index_col=0)#指定0列为index列
		return df

	def get_D_k(self,code,type1):
		df=0
		return df 

#数据存储接口
class gu_save:
	#存入数据
	def save_to_db(self,df,type1):
		return 0
	#存入csv
	def save_to_csv(self,df,files1,mode):
		#files1=gu_jiekou_fuzhu().get_csvname(code)
		if df.empty:return 0
		if mode=='a' and os.path.exists(files1):
			df.to_csv(files1,mode='a',header=False)
			print('- 增量存入csv')
		else :
			df.to_csv(files1)
			print('- 覆盖存入csv')
		return 1
#辅助功能
class gu_fuzhu:

	#代码补全处理
	def code_buquan(self,code):

		strZero = ''
		for i in range(len(str(code)), 6):
			strZero += '0'

		code1=strZero + str(code)
		if code1[0]=='6':
			code2=code1+'.SH'
		else:
			code2=code1+'.SZ'
		return code2
	#
	def get_csvname(self,code):
		co=self.code_buquan(code)
		csv_path='d:/stock_csv/{}.csv'.format(co)
		return csv_path

	#计算复权因子
	def get_fuquanyinzhi(self,code):

		return 0


#策略
#策略1存入csv
#策略2存入db
#策略3获取新api增量数据
#策略4获取旧api
#策略5获取本地from db
#策略6获取本地from csv
class t(gu_getfromapi,gu_save):
	
	def test1(self):
		code1='600609'
		files1=gu_fuzhu().get_csvname(code1)
		mode='a' if os.path.exists(files1) else ''
		#mode='a'
		#获取
		df[df[date].isin()]

		df=self.get_D_k(gu_fuzhu().code_buquan(code1),'')

		print(code1,files1,mode)
		self.save_to_csv(df,files1,mode)
		#ll=df.values
		return 0
	



if __name__ == '__main__':
	#输入股票代码获取该代码的基础信息
	#print(gu_save.__doc__)
	t().test1()
	#df=gs.get_base_from_api()
	#print(df.head(),len(df))
	#print(gu_jiekou_fuzhu().get_csvname('002498'))

