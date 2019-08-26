#gupiaoClass
#股票类
import tushare as ts
import datetime
class gupiaoClass(object):
	"""docstring for gupiaoClass
		股票类
	"""
	def __init__(self, arg):
		super(gupiaoClass, self).__init__()
		self.arg = arg
		self.code=arg
		print(arg)
	#获取股票基础信息
	def get_jcxx(self):
		pass

	#获取股票历史k线
	def get_k(self):
		pass

	#存储K线
	def save_k(self):
		pass

	#存储基础信息
	def save_jcxx(self):
		pass

	#删除K线
	def _delete_k(self):
		pass

	#判断是否一致K线
	def _issameK(self):
		pass

	#提取信息
	def select_k(self):
		pass
		
	def select_jcxx(self):
		pass