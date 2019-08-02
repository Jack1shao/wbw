#数据分析

class sjfenxClass(object):
	"""docstring for sjfenx
	def __init__(self, arg):
		super(sjfenxClass, self).__init__()
		self.arg = arg
	"""
	#必发数据分析
	def bfsjfx(self,datelist):
		fxlist=[]
		#print(datelist)
		for li in datelist:
		
			if int(li[1])==2:
				
				if  float(li[10])<23:fxlist.append("必发平局分析：大冷")
				if  float(li[10])>=23 and float(li[10])<30 :fxlist.append("必发平局分析：过冷")
				if  float(li[10])>=30: fxlist.append("必发平局分析：热")

		return fxlist
	#必发数据提点分析
	def bfsjtdfx(self,datelist):
		return datelist[0][3],datelist[0][4],datelist[0][2]
		pass
	#欧指数据分析
	def ozsjfx(self,datelist):
		#print(datelist)
		fxlist=[]
		for li in datelist:
			if li[2]=='Iceland':
				#19:ck0\15:chf\5:cz0
				#print(li)
				if float(li[19])*100-float(li[15])>=-0.1 or float(li[18])*100-float(li[15])>=-0.1:
					fxlist.append("赔付不正常") 
				if float(li[19])*100-float(li[15])<-0.1 and float(li[18])*100-float(li[15])<-0.1:
					fxlist.append("赔付正常") 
				if float(li[15])<=80.10:
					fxlist.append("初返还低") 
				else:fxlist.append("初返还高") 
				break

		return fxlist