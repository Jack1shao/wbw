

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

	def _bsid_from_db(self,idstart,idend,sql):
		#sql="select idnm from scb where idnm between " +str(idstart)+" and " +str(idend)
		sv=savedateClass().select(sql)
		return  sv
	#补齐必发信息
	def bqbf(self,id1):
		print('开始获取必发',id1)
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
			return 0
		return 1

	#获取单场信息
	def getbs(self,id1):
		print('开始获取',id1)
		dates=savedateClass()
		hs=htmlsoup(id1)

		scblist,bzsc=hs.getsc()
		if bzsc==0:
			print("无赛程")
			scberrorsql="insert into scb_error values (%s,%s)"
			liste=[]
			listee=[]
			liste.append(str(id1))
			liste.append("无赛程")
			listee.append(liste)

			dates.insert(listee,scberrorsql)
			return 0

		ozlist,bzoz=hs.getouzhi()
		yplist,bzyp=hs.getyapan()
		bflist,bzbf,bflist_sjtd=hs.getbifa()

		if bzsc*bzoz*bzyp==0: print('no date ,return');return 0

		print('写入数据库....')
		
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
			else:
				print('no date ,写入必发空值')
				dates.insert(bflist,bfsql)#写入必发空值

		return 1
	#补齐必发
	def bqbfmain(self,idstart,idend):
		jsq=0#计数器
		list1=[]
		if idstart>idend:return 0
		#必发不存在的记录
		#sql="select idnm from scb s where not EXISTS (select 1 from bifa b where b.idnm=s.idnm)"
		#		+" and idnm between " +str(idstart)+" and " +str(idend)
		ypgs='Bet365'
		jp1='受半球'
		sql="SELECT s.idnm from scb s ,yapan y  where s.idnm=y.idnm and y.ypgs='"+ypgs+"' and y.jp='"+jp1+"' and not EXISTS (select 1 from bifa b where b.idnm=s.idnm)"
		#print(sql)
		idlist=self._bsid_from_db(idstart,idend,sql)

		for idnmrow in idlist:
				for idnm0 in idnmrow:
					list1.append(idnm0)
					self.bqbf(idnm0)
				print(datetime.datetime.now())
		for x in range(idstart,idend+1):
			if x  in list1:
				jsq=jsq+1
				#self.bqbf(x)
				print(datetime.datetime.now())
		return 0
	#获取比赛数据
	def getbsid(self ,idstart,idend):


		jsq=0#计数器
		list1=[]
		if idstart>idend:return 0
		sql="select idnm from scb_error union all select idnm from scb where  idnm between "+str(idstart)+" and " +str(idend)
		idlist=self._bsid_from_db(idstart,idend,sql)
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
list2=[778990,778998,779000]
for x in list2:	h.getbsid(x,x)
#h.getbsid(826637,826637)

#h.bqbfmain(714214,714604)
#['丹超','19','805215','805245']
#['瑞典超','19','789008','789280']
#['瑞典超','17','633991','634230']
#['瑞典超','18','707696','707863']

#['挪超','17','630624','630863']
#['荷甲','17','663521','663826']
#['丹超','17','665106','665287']
#['俄超','17','666163','666402']
#['芬超','18','719170','719343']
#['西甲','18','748619','748992']
#['西甲','17','687452','687831']

#['巴甲','18','718526','718813']
#['巴甲','19','800197','800357']
#['巴乙','17','659768','660147']
#['美职','18','714214','714604']
#['美职','19','780198','780588']

#['英超','18','730907','731285']
#['英超','17','663128','663507']


#['意甲','18','749789','750164']
#['意甲','17','690000','690378']
#['德乙','18','738015','738320']
#['德乙','17','673226','673531']
#['法乙','18','730388','730767']
#['法乙','17','665289','665667']
#['k1联','18','715319','715488']
#['k1联','19','783817','784031']

#['日职','17','647803','648108']
#['日职','18','711444','711749']
#['日职','19','779376','779644'] 
#['日乙','18','713219','713588']

#['德甲','18','737551','737856']
#['德甲','17','672920','673225']
#['德甲','16','596166','596471']
#['德甲','15','524841','525145']
#['德甲','14','437133','437438']
#['德甲','13','397709','398014']
#['法甲','18','729204','729582']
#['法甲','17','664725','665104']
#['法甲','16','573789','574160']
#['法甲','15','522881','523257']
#['法甲','14','435091','435470']
#['法甲','13','398015','398394']
#[]

