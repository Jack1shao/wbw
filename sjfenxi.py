#数据分析
from htmlsoupClass import htmlsoup
from readexcle import readExcle
from collections import Counter
from savedateClass import savedateClass
class sjfenxClass(object):
	
	def __init__(self, arg):
		super(sjfenxClass, self).__init__()
		self.arg = arg
		self.id1=int(arg)
	#获取必发数据
	def _getbf(self):
		sql='select * from bifa y where y.xh>0 and y.idnm={}'.format(self.id1)
		sql2='select * from sjtdbf y where y.idnm={}'.format(self.id1)
		bflist=savedateClass().select(sql)
		bflist_sjtd=savedateClass().select(sql2)
		bzbf=1
		#print(len(ozlist))
		if len(bflist)==0:
			hs=htmlsoup(self.id1)
			bflist,bzbf,bflist_sjtd=hs.getbifa()
		return bflist,bzbf,bflist_sjtd
	def _getoz(self):
		sql='select * from ouzhi y where y.idnm={}'.format(self.id1)
		ozlist=savedateClass().select(sql)
		bzoz=1
		#print(len(ozlist))
		if len(ozlist)==0:
			hs=htmlsoup(self.id1)
			ozlist,bzoz=hs.getouzhi()

		return ozlist,bzoz
	def _getsc(self):
		sql='select * from scb y where y.idnm={}'.format(self.id1)
		scblist=savedateClass().select(sql)
		bzsc=1
		#print(len(scblist))
		if len(scblist)==0:
			hs=htmlsoup(self.id1)
			scblist,bzsc=hs.getsc()
		return scblist,bzsc

	def _getyp(self):
		sql='select * from yapan y where y.idnm={}'.format(self.id1)
		#print(sql)
		yplist=savedateClass().select(sql)
		bzyp=1
		#print(len(yplist))
		if len(yplist)==0:
			hs=htmlsoup(self.id1)
			yplist,bzyp=hs.getyapan()
		return yplist,bzyp

	#必发数据分析
	def bfsjfx(self):
		bflist,bzbf,bflist_sjtd=self._getbf()
		
		#print(datelist)
		#容错
		fxlist=[]
		if bzbf==0:return fxlist,0
		#分析
		for li in bflist:
			if int(li[1])==2:
				#print(li)
				if  float(li[12])<20:fxlist.append("必发平局分析：大冷")
				if  float(li[12])>=20 and float(li[12])<30 :fxlist.append("必发平局分析：过冷")
				if  float(li[12])>=30: fxlist.append("必发平局分析：热")
		#必发数据提点分析
		#print(bflist_sjtd[0][4].find("必发"))
		if bflist_sjtd[0][4].find("平局交易过冷")>=0:
			fxlist.append("数据提点分析：平局交易过冷")
		else:fxlist.append("数据提点分析：其他")
		fxlist.append(bflist_sjtd[0][3])
		#print(fxlist)
		return fxlist,1
	
		
	#欧指数据分析
	def ozsjfx(self):
		#print(datelist)
		ozlist,bzoz=self._getoz()

		fxlist=[]
		for li in ozlist:
			if li[2]=='Iceland':
				#19:ck0\15:chf\5:cz0
				#print(li)
				if float(li[19])*100-float(li[15])>=-0.1 or float(li[18])*100-float(li[15])>=-0.1:
					fxlist.append("Iceland赔付不正常") 
				if float(li[19])*100-float(li[15])<-0.1 and float(li[18])*100-float(li[15])<-0.1:
					fxlist.append("Iceland赔付正常") 
				if float(li[15])<81:
					fxlist.append("Iceland初返还低") 
				else:fxlist.append("Iceland初返还高") 

				if float(li[5])<4:
					fxlist.append("Iceland负赔低-低于4")
				else: fxlist.append("Iceland负赔高-高于4")
				break

		return fxlist,1
	#分析主程序	
	def bd(self):

		#不是半球盘不分析
		yplist,bzyp=self._getyp()
		bz2=[x for x in yplist if x[2]=='Bet365' and x[4]=='半球']
		if len(bz2)==0:return 0
		#取必发和欧指数据
		bffxlist,bzbf=self.bfsjfx()
		ozfxlist,bzoz=self.ozsjfx()
		#容错
		if bzbf*bzoz==0 or len(ozfxlist)*len(bffxlist)==0:print("date lost ...");return 0
		#与已有数据比对
		df,l=readExcle('e:/05iceland.xlsx').read()
		x=0
		li=[]
		for i,row in df.iterrows():
			if row['ykzs']==bffxlist[0] and row['kl']==ozfxlist[0] and row['peifu']==ozfxlist[1] and row['fupei']==ozfxlist[2] and row['bss2']==bffxlist[2]:
				x+=1
				li.append(row['sg'])
			#print(row)
		res=Counter(li)

		scblist,bzsc=self._getsc()
		
		listreturn=[]
		listreturn.extend(scblist[0])
		listreturn.extend(ozfxlist)
		listreturn.extend(bffxlist)
		print(scblist[0])
		print(bz2[0][4])
		print(ozfxlist+bffxlist)
		print(self.id1,res)
		return listreturn,res

list1=['816941']
[sjfenxClass(x).bd()  for x in list1 if len(list1)>0]
#[print(x) if x>10 else print(0) for x in range(1,10) ]
