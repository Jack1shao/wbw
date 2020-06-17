#stockmd.py
#基础
import os
from pandas import read_csv
from abc import ABCMeta, abstractmethod
class stock(object):
	"""docstring for stockclass"""
	def __init__(self, arg):
		super(stock, self).__init__()
		#参数为股票代码
		self.arg = arg
		#补全股票代码
		s_n=''
		ss=str(arg)[-6:]
		for i in range(len(ss), 6):
			s_n+='0'

		self.code=s_n+ss
		#k线数据
		self.df=None

		
	#修饰器函数
	def decorator(self,component):
		self.component=component
	#获取股票代码
	def getcode(self):
		return self.code
	#获取股票名称
	def getname(self):
		bacs='basc'
		df=None
		csv_path='d:/stock_csv/{}.csv'.format(bacs)
		files1=csv_path
		if os.path.exists(files1):
			with open(files1,'r',encoding='utf-8') as csv_file:
				df = read_csv(csv_file,index_col=0)#指定0列为index列

		if df.empty:
			return ''
		
		for cod,row in df.iterrows():
			#要补全6位？？？
			if str(cod)==self.code:
				return row[0]
		print('未找到股票名字')	
		return ''
		

	#市值，根据日线
	def get_sz(self):
		code1=self.code
		df=self.get_k_from_csv(code1,'D')
		high=df[-1:].high.values.tolist()
		#print(high)
		df2=self.get_base_from_db()
		totals=df2.loc[int(code1)].totals
		sz=totals*high[0]
		#print(float('%.2f' % sz),'亿')#小数位数
		return float('%.2f' % sz)

	def getk(self):
		print('1111getk')
		self.df=self.component.getk()+self.arg
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

s=stock('600609')
print(s.getname())
print(s.code)
m_kl=m_kl()
w=w_kl()
#m_kl.decorator(w_kl)
s.decorator(w)

s.getk()
print(s.df)
print('---1')
s=stock('600609')
s.decorator(w)


print(s.df)
print('---2')
s.getk()
print(s.df)
#s.getname()
		
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

