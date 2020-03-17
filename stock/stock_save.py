#stock_save
from getstockClass import getstock
from pandas import read_csv
import os
from pandas.core.frame import DataFrame

class stock_saveClass(object):
	"""docstring for stock_saveClass"""
	def __init__(self, arg):
		super(stock_saveClass, self).__init__()
		self.arg = arg
		self.code=arg
		self.path1='d:/stock_csv/'
		self.files1='{0}{1}.csv'.format(self.path1,self.code)

	def stock_to_csv(self):
		k=getstock(self.code)
		df=k.GET_KLINE(self.code,'D','0000-05-04','0000-05-04')
		name=k.GET_BASE()
		if df.empty:
			print("empty")
			return 0
		#files1='{0}{1}.csv'.format(self.path1,self.code)
		#print(files1)
		df.to_csv(self.files1)
		print('-{}-{} 存入csv'.format(self.code,name))
		return 1

	def stock_to_db(self,df):

		pass

	def stock_from_csv(self):
		
		if os.path.exists(self.files1):
			with open(self.files1,'r',encoding='utf-8') as csv_file:
				df = read_csv(csv_file,index_col=0)#指定0列为index列
		else:
			print('未找到股票数据，请先载入')
			return DataFrame([])
		return df

	def stock_from_db(self,df):
		return []

		
	def append(self,df,files1):
		df.to_csv(files1,mode='a',header=False)
		return 1	

'''li=['300498','002385','300313']
k=stock_saveClass('300313')
k.stock_to_csv()
df=k.stock_from_csv()
print(df.head())'''