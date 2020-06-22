import os
from pandas import read_csv

class csv_op:
	#'''通用'''
	def get_from_csv(self,files1):
	
		if os.path.exists(files1):
			with open(files1,'r',encoding='utf-8') as csv_file:
				df = read_csv(csv_file,index_col=0)#指定0列为index列
		return df

