#stockmd.py
#基础
from abc import ABCMeta, abstractmethod
class stock(object):
	"""docstring for stockclass"""
	def __init__(self, arg):
		super(stock, self).__init__()
		self.arg = arg
		self.df='Non1e'
	def decorator(self,component):
		self.component=component

	def getcode():
		pass

	def getname(self):
		print(self.df+'getname')
		

	def getsz():
		pass

	def getk(self):
		print('1111')
		self.df=self.component.getk()+'111'
		return self.component.getk()+'rrr'
		
#装饰类
class Finery():
	def __init__(self):
		self.component=None

	def decorator(self,component):
		self.component=component

	__metaclass__=ABCMeta

	@abstractmethod
	def getk(self):
		if self.component:
			self.component.getk(self)

class m_kl(Finery):
	def getk(self):
		Finery.getk(self)
		print('m_kl')
	
class w_kl(Finery):
	def getk(self):
		Finery.getk(self)
		print('w_kl')
		return 'w_kl'

s=stock('002498')
m_kl=m_kl()
w=w_kl()
#m_kl.decorator(w_kl)
s.decorator(w)

df=s.getk()
print(df)
s.getname()
		
#命令
class commandclass(object):
	"""docstring for commandclass"""
	def __init__(self, arg):
		super(commandclass, self).__init__()
		self.arg = arg
		

#策略
class celvclass(object):
	"""docstring for celvclass"""
	def __init__(self, arg):
		super(celvclass, self).__init__()
		self.arg = arg
	
	def bc9():
		pass

	def rs100():
		pass

