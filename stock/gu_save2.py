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

class gu_save2:
	'''获取数据'''
	#获取api 数据
	def get_from_api(self,type1):
		df=0

		return df

	#存入数据
	def save_to(self,df,type1):

		return 0

	#获取本地数据
	def get_from_bd(self,code,type1):
		df=0

		return df 
	#计算复权因子
	def get_fuquanyinzhi(self,code):

		return 0

	#代码补全处理
	def code_buquanchuli(self,code):

		return code
	#
	def get_csvmc(self,code):
		csv_path='d:/stock_csv/{}.csv'.format(code)
		return csv_path
	
	#存入csv
	def save_k_to_csv(self,code,df,mode,ktype1):
		files1=self.get_csvmc(code+ktype1)
		if mode=='a' and os.path.exists(files1):
			df.to_csv(files1,mode='a',header=False)
			print('- 增量存入csv')
		else :
			df.to_csv(files1)
			print('- 覆盖存入csv')
		return 1
	#获取基础数据api
	#获取基础数据db
	def get_base_from_api(self):
		df = ts.get_stock_basics()
		return df

	#基础数据2
	def get_base_from_db(self):
		basc='basc'
		files1=self.get_csvmc(basc)
		if os.path.exists(files1):
			with open(files1,'r',encoding='utf-8') as csv_file:
				df = read_csv(csv_file,index_col=0)#指定0列为index列
		return df

#策略
#策略1存入csv
#策略2存入db
#策略3获取新api增量数据
#策略4获取旧api
#策略5获取本地from db
#策略6获取本地from csv

if __name__ == '__main__':
	#输入股票代码获取该代码的基础信息
	print(gu_save2.__doc__)
	gs=gu_save2()
	df=gs.get_base_from_api()
	print(df.head(),len(df))

