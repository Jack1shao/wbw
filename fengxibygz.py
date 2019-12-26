
#通过规则分析
#fengxibygz()
from zqconfigClass import zqconfigClass
from zqfenxi_gz import zqfenxi_gz
import math
class fengxibygz(object):
	"""docstring for fengxibygz"""
	def __init__(self, arg):
		super(fengxibygz, self).__init__()
		self.arg = arg
		self.file1='e:/半球.csv'
	def __list_gz(self):
		list_gz=['半球','规则1',	['count_len','要',6,7,8,9],['count_len','要']]

		return list_gz
	def __get_df(self):
		df_idnm=zqconfigClass(0).select(self.file1)

		return df_idnm
	


	def t(self):
		df=self.__get_df()
		df=df[(df.count_len)==0]
		kk=zqfenxi_gz()
		listsg=list(df.sg.values)
		print(kk.jslsd(listsg))
		print(df)
		return 0


#k=fengxibygz(0)
#print(int(4.1))
#k.t()		