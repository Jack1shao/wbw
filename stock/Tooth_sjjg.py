#tooth
#数据结构
#1、队列
class queue:
	'''先进先出队列'''
	def __init__(self,maxsize=0):
		self.maxsize=maxsize
		self.__list=[]
	def put(self,item):
		if len(self.__list)>=self.maxsize:
			self.__list.pop(0)
		self.__list.append(item)
		return 0

	def get(self):
		return self.__list