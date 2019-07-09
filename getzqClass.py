

'''
	从网页获取数据
'''
from savedateClass import savedateClass
from htmlsoupClass import htmlsoup
import datetime

class getzqClass(object):
	"""docstring for getzqClass"""
	def __init__(self, arg):
		super(getzqClass, self).__init__()
		self.arg = arg

	def _bsid_from_db(self,idstart,idend):
		sql="select idnm from scb where idnm between " +str(idstart)+" and " +str(idend)
		sv=savedateClass().select(sql)
		return  sv
	#获取单场信息
	def getbs(self,id1):
		print('开始获取',id1)

		hs=htmlsoup(id1)

		scblist,bzsc=hs.getsc()
		ozlist,bzoz=hs.getouzhi()
		yplist,bzyp=hs.getyapan()
		bflist,bzbf,bflist_sjtd=hs.getbifa()

		if bzsc*bzoz*bzyp==0: print('no date ,return');return 0

		print('写入数据库....')
		dates=savedateClass()
		scbsql="insert into scb values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		ypsql="insert into yapan values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		ozsql="insert into ouzhi values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		
		bfsql="insert into bifa values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		bfsql_sjtd="insert into sjtdbf values (%s,%s,%s,%s,%s)"
		
		
		t=dates.insert(scblist,scbsql)#写入赛程
		if t==1:
			dates.insert(ozlist,ozsql)#写入欧指
			dates.insert(yplist,ypsql)#写入亚盘

			if bzbf==1:
				dates.insert(bflist,bfsql)#写入必发
				dates.insert(bflist_sjtd,bfsql_sjtd)#写入必发-数据提点

		return 1

	def getbsid(self ,idstart,idend):
		
		jsq=0#计数器
		list1=[]
		if idstart>idend:return 0
		idlist=self._bsid_from_db(idstart,idend)
		for idnmrow in idlist:
				for idnm0 in idnmrow:
					list1.append(idnm0)
		#print(list1)
		for x in range(idstart,idend+1):
			if x not in list1:
				jsq=jsq+1
				self.getbs(x)
				print(datetime.datetime.now())


		print(datetime.datetime.now())
		return 0
h=getzqClass('')
#h.getbs(779440)
h.getbsid(435091,435470)

