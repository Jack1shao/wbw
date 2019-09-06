#tooth_excle
#读取电子表格
import pandas
class tooth_excleClass(object):
	"""docstring for tooth_excleClass"""
	def __init__(self, arg):
		super(tooth_excleClass, self).__init__()
		self.arg = arg
		self.filesname=arg

	def write(self,df):
		pass

	def read(self):
		filespath=self.arg
		#filespath='e:/0.5.xlsx'
		with pandas.ExcelFile(filespath) as excelfiles1:
			df= pandas.read_excel(excelfiles1,sheet_name=0)
		excelfiles1.close()
		return df
#h=tooth_excleClass('e:/0.5.xlsx')
#h.read()
		