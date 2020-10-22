'''获取数据'''
import tushare as ts
import datetime
import os
from pandas import read_csv
from pandas.core.frame import DataFrame
from collections import namedtuple

#
Stock=namedtuple('Stock','code name hangye totals files1')
ts.set_token('4d4e8c66f3fe804a585a345419362a9982790682a79ef65214b5d5e1')
#数据获取接口
class gu_getfromapi:
	'''从api获取数据'''
	#获取api 数据
	def api_D_k(self,code1,start_day):
		
		'''新的接口Pro'''
		pro = ts.pro_api()
		#日期处理
		rq_now = datetime.datetime.now().strftime('%Y%m%d')
		rq_kaishi='20140103'
		start_d=rq_kaishi if start_day=='' else start_day
		#获取数据
		df=pro.daily(ts_code=code1, start_date=start_d, end_date=rq_now)
		df.rename(columns={'vol':'volume','trade_date':'date','ts_code':'code'}, inplace=True) 
		df=df.sort_values(by='date' , ascending=True)
		return df

	#全天模式
	def api_allday_k(self,date):
		ff
		return df
	#获取基础数据api
	def api_base(self):
		df = ts.get_stock_basics()
		rq_now = datetime.datetime.now().strftime('%Y%m%d')
		df['gxrq']=rq_now

		return df

class gu_getfromdb(object):
	"""获取本地数据"""
	#获取本地文件数据
	def get_fromfiles(self,files1):
		
		print('来自{1}类--从本地文件{0}取数--'.format(files1,self.__class__.__name__))
		
		if os.path.exists(files1):
			with open(files1,'r',encoding='utf-8') as csv_file:
				df = read_csv(csv_file,index_col=0)#指定0列为index列
		else:
			print('未找到数据，请先载入')
			return DataFrame([])
		return df
		

#数据存储接口
class gu_save:
	#存入数据
	def save_to_db(self,df,type1):
		return 0
	#存入csv
	def save_tofiles_by_df(self,df,files1,mode):
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
		if code=='basc':
			csv_path='d:/stock_csv/{}.csv'.format(code)
		else:	
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
class t(gu_getfromapi,gu_save,gu_getfromdb):
	#存储基础数据
	def savebasc(self):
		'''存储基础数据'''
		print('存储基础数据')
		code1='basc'
		files1=gu_fuzhu().get_csvname(code1)
		mode=''
		df=self.api_base()
		bb=self.save_tofiles_by_df(df,files1,mode)
		return bb
	#K线增量存储
	def D_k_add(self,code1):
		#code1='600609'
		files1=gu_fuzhu().get_csvname(code1)
		#文件存在，则为增量 修改模式
		mode='a' if os.path.exists(files1) else ''
		#mode='a'
		if mode=='a':
			df1=self.get_fromfiles(files1)#获取本地df
			date_li=df1.date.values.tolist()#日期列
			date_max=max(date_li)#最大日期
			
			start_d=str(date_max+1)
		else:
			start_d='20140101'
		#获取api ‘D’ k线
		df=self.api_D_k(gu_fuzhu().code_buquan(code1),start_d)
			#转为字符串
	
		if df.empty:
			print('增量为空Df 00001')
			return 1
		else:
			self.save_tofiles_by_df(df,files1,mode)
			return 0
	#单日全量存储
	def D_k_add_oneday(self,date):
		#数据存在，存入文件，并添加交易日历

		#文件存在，则添加

		pass
	#获取交易日历
	def jiaoyirili(self):
	 	'''根据5只代表票获得交易日历'''
	 	#[]
	 	pass

	
#生成复权数据 
class fq:

	def qfq(self):
		pass

	def hfq(self):

		pass



if __name__ == '__main__':
	#输入股票代码获取该代码的基础信息
	#print(gu_save.__doc__)
	code1='600609'
	t().savebasc()
	t().D_k_add(code1)
	#df=gs.api_base_from_api()
	#print(df.head(),len(df))
	#print(gu_jiekou_fuzhu().get_csvname('002498'))

