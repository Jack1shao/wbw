from sklearn import datasets
import pandas as pd
import mglearn
from operClass import file_op
class dataset_gu():
	'''用于学习的数据'''

	def get_date(self):
		file1='d:/aiyb2020.csv'
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
df=d.get_date()

y=df.columns[-2:]
print(df[y].head())
