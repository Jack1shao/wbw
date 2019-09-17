
#补充数据库数据
from savedateClass import savedateClass
from htmlsoupClass import htmlsoup
import datetime
#补齐未进入数据库的数据
class buqisj(object):
	"""docstring for buqisj"""
	def __init__(self, arg):
		super(buqisj, self).__init__()
		self.arg = arg
	#	#判断是否数据库中存在必发数据
	def isin_bf(self,idnm):
		sql='select * from bifa y where y.xh>0 and y.idnm={}'.format(int(idnm))
		sql2='select * from sjtdbf y where y.idnm={}'.format(int(idnm))
		bflist=savedateClass().select(sql)
		bflist_sjtd=savedateClass().select(sql2)
		if  len(bflist)==0:
			return 0
		return 1

	#补齐必发信息	#补齐必发
	def bqbf(self,id1):
		print('开始获取必发',id1)
		if self.isin_bf(id1)==1:
			print(id1,'有必发数据在数库中')
			return 0

		hs=htmlsoup(id1)
		bflist,bzbf,bflist_sjtd=hs.getbifa()
		print('写入数据库....')
		dates=savedateClass()
		bfsql="insert into bifa values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		bfsql_sjtd="insert into sjtdbf values (%s,%s,%s,%s,%s)"

		if bzbf==1:
			dates.insert(bflist,bfsql)#写入必发
			dates.insert(bflist_sjtd,bfsql_sjtd)#写入必发-数据提点
		else:
			print('no date ,写入必发空值')
			dates.insert(bflist,bfsql)#写入必发空值
			return 2
		return 1
	#补齐必发
	def bqbfmain(self,idstart,idend):
		jsq=0#计数器
		#必发不存在的记录
		sql="SELECT s.idnm from scb s where  s.nd=18 and not EXISTS (select 1 from bifa b where b.idnm=s.idnm) limit 30"
		idlist=savedateClass().select(sql)
		#补齐在列表Idlist 中的比赛必发数据
		iii=0
		for idnmrow in idlist:
				for idnm0 in idnmrow:
					print(iii,idnm0)
					if self.bqbf(idnm0)>0:
						iii+=1
						if iii>60:return 0
				print(datetime.datetime.now())
		return 0

#h=buqisj('').bqbfmain(1,2)

