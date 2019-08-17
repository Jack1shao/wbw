import time
import xlrd
#import xlsxwriter
import pandas
import os
#
class readExcle(object):
	"""docstring for readExcle
		读取电子表格
	"""
	def __init__(self, arg):
		super(readExcle, self).__init__()
		self.arg = arg

	#读取电子表格返回dateframe
	def read(self):
		filespath=self.arg
		filespath='e:/05iceland.xlsx'

		#print(os.listdir('e:'))
		with pandas.ExcelFile(filespath) as excelfiles1:
			
			data= pandas.read_excel(excelfiles1,sheet_name=0)
		#print(len(data))
		#for i,row in data.iterrows():			print(row['s2'])
		excelfiles1.close()
		#
		return data,len(data)

#filespath='e:/5iceland1112.xls'
#h=	readExcle(filespath)
#h.read()
