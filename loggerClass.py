#单列模式
#2019-06-25
#
import datetime
class logger(object):
	"""docstring for logger
	日志记录器
	"""
	
	#私有类	
	class _singlelogger():
		"""docstring for _singlelogger"""
		def __init__(self):
			self.val=None
			
		def __str__(self):
			return "{0!r} {1}".format(self,self.val)
		
		#测试用——————————————————————	
		def p(self):
			print(self.val)

		#内部函数，写入功能	
		def _write_log(self,level):
			#打开或新建log文件
			with open("./loggerclass.log","a") as log_file:
				log_file.write("{0} {1} {2}\n".format(datetime.datetime.now(),level,self.val)) #写入格式字符
		#写入类别
		def error(self):
			self._write_log("error")
			self.p()
		
		def info(self):
			self._write_log("info")
			self.p()	
		

	instance=None
	def __new__(cls):
			if not logger.instance:
				logger.instance=logger._singlelogger()

			return logger.instance

	def __getattr__(self,name):
			return getattr(self.instance,name)

	def __setattr__(self,name):
			return setattr(self.instance,name)	
