import time
import xlrd
import xlsxwriter

#一个打开excel和写入excel的类
class ctrl_excel(object):
	"""docstring for ctrl_excel"""
	def __init__(self, arg):
		super(ctrl_excel, self).__init__()
		self.arg = arg

	def open_excel(excelfilepath):
		with xlsxwriter.Workbook(excelfilepath) as work:
			tablelist = work.sheets()[1]#获取sheets
		
		return tablelist

	def write_excel(rowlist):

		excelfilepath='e:/123456.xls'
		with xlsxwriter.Workbook(excelfilepath) as work:
			worksheet = work.add_worksheet('123')
			for x,v in enumerate(rowlist):
				for y,v2 in enumerate(v):
					worksheet.write(0,y,y)#构造表格标题
					worksheet.write(x+1,y,v2)#对list遍历并按坐标写入excel

		work.close()
		return 0
	
	def pandasRd_excel(filespath):
		filespath='e:/football/1819/1/纽伦堡VS美因茨(德甲)欧洲数据.xls'
		with pandas.ExcelFile(filespath) as excelfiles1:
			data= pandas.read_excel(excelfiles1,sheetname=1)
		print(data)

		excelfiles1.close()
		return 0