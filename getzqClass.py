

'''
	从网页获取数据
	主程序
'''
from savedateClass import savedateClass
from htmlsoupClass import htmlsoup
import datetime

class getzqClass(object):
	"""docstring for getzqClass"""
	def __init__(self, arg):
		super(getzqClass, self).__init__()
		self.arg = arg

	#获取数据库中批量比赛id
	def _bsid_from_db(self,idstart,idend,sql):
		#sql="select idnm from scb where idnm between " +str(idstart)+" and " +str(idend)
		sv=savedateClass().select(sql)
		return  sv

	#获取单场信息
	def getbs(self,id1):
		print('开始获取',id1)
		dates=savedateClass()
		hs=htmlsoup(id1)

		scblist,bzsc,ozlist=hs.getscbandouzhi()
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
		bzoz=bzsc
		#ozlist,bzoz=hs.getouzhi()
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
	#获取数据库中批量比赛id_to list
	def getbsid_bylist(self,list1):
		#list1=[779110,779824]
		if len(list1)==0:return 0
		sql="select s.idnm from scb s where s.idnm in {}".format(tuple(list1))
		list_idnm=savedateClass().select(sql)
		return list_idnm
	#获取比赛段的数据
	def getbsid(self ,idstart,idend):

		iii=0#计数器
		list1=[]

		#容错机制
		if idstart==None:return 0
		if abs(idend-idstart)>1000 : print("idstart-idend>500"); return 0
		if idstart>idend:print("idstart>idend"); return 0

		#获取数据库中已有的比赛id，
		#这些比赛不在从网页获取
		sql="select idnm from scb_error where idnm between {0} and {1} union all select idnm from scb where  idnm between {0} and {1}".format(idstart,idend)
		idlist=self._bsid_from_db(0,0,sql)
		for idnmrow in idlist:
			for idnm0 in idnmrow:
				list1.append(idnm0)
		#获取还未进入数据库的比赛
		for x in range(idstart,idend+1):
			if x not in list1:
				iii=iii+1
				self.getbs(x)
				if iii>20:break
				print(datetime.datetime.now(),'--->',iii,'<---')
		print('<<<...',datetime.datetime.now(),'--->',iii,'<---')
		return iii
	#补齐之前整个联赛的比赛数据
	def getbs_othor(self,ls,nd):
		#获取该联赛最小idnm 和最大id，补齐比赛数据
		
		idstart=0	
		minidnm_sql="SELECT min(idnm) from scb where nd='{}' and ls='{}'".format(nd,ls)
		maxidnm_sql="SELECT max(idnm) from scb where nd='{}' and ls='{}'".format(nd,ls)
		print(minidnm_sql,maxidnm_sql)
		minid=savedateClass().select(minidnm_sql)
		maxid=savedateClass().select(maxidnm_sql)
		idstart=minid[0][0]
		idend=maxid[0][0]
		#print("补齐之前比赛的数据{}-{}".format(idstart,idend))
		#print(minid[0][0],maxid[0][0])
		iii=0
		if idstart and idend:
			print("补齐比赛数据:{}{}赛季-->({}-{})<---".format(ls,nd,idstart,idend))
			iii=self.getbsid(idstart,idend)
			print('--->{}<---'.format(iii))
		return iii
	#主程序入口
	'''def getzq_main(self):
					between_list=[
							['法甲','19','808039','808071'],
							['法乙','19','809429','809483'],
							['英超','19','806501','806519'],
							['西甲','19','830801','0'],
							['意甲','19','853822','0'],
							['德乙','19','825597','825627'],
							['德甲','19','824571','0'],
							['芬超','19','795956','0'],
							['挪超','19','788508','0'],
							['k1联','19','783817','784125'],
							['日职','19','779376','779788'], 
							['美职','19','780198','780808'],
							['日职乙','19','778452','779044'],
							['丹超','19','805215','805245'],
							['巴甲','19','800197','800473'],
							['丹甲','19','0','0'],
							['葡超','19','837459','0'],
							['瑞士超','19','0','0'],
							['瑞典超','19','789008','789280'],
							['荷甲','19','0','0']
						]
			
					in_list=['779816','805581','867116','867116']	
					if len(in_list)!=0:
						print(in_list)
						for x in in_list:
							self.getbsid(int(x),int(x))
					#补齐比赛数据
					iii=0
					for x in between_list:
						iii+=1
						
						#if x[0]!='日职乙':continue
						self.getbs_othor(x[0],x[1])
					return 0'''

#h=getzqClass('').idnm_in([])

#h=getzqClass('').getzq_main()
#print(h.bqbf(800355))

#补齐必发数据，没有必发数据时，加入必发数据
#h.bqbfmain(714214,714604)
#['k1联','19','783817','784031']
#['日职','19','779376','779644'] 
#['美职','19','780198','780588']
#['日乙','19','778452','779044']
#['丹超','19','805215','805245']
#['巴甲','19','800197','800357']
#['瑞典超','19','789008','789280']
#['芬超','19','0','0']
#['西甲','19','0','0']
#['意甲','19','0','0']
#['德乙','19','0','0']
#['德甲','19','824571','0']
#['法甲','19','808039','808055']
#['法乙','19','809429','809483']
#['英超','19','806501','806519']
#['丹超','18','729966','730147']
#['荷甲','18','731287','731591']
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
#['巴乙','17','659768','660147']
#['美职','18','714214','714604']
#['英超','18','730907','731285']
#['英超','17','663128','663507']
#['英超','16','572731','']
#['英超','15','0','']
#['英超','14','0','']
#['英超','13','0','']
#['意甲','18','749789','750164']
#['意甲','17','690000','690378']
#['德乙','18','738015','738320']
#['德乙','17','673226','673531']
#['法乙','18','730388','730767']
#['法乙','17','665289','665667']
#['k1联','18','715319','715488']
#['日职','17','647803','648108']
#['日职','18','711444','711749']
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