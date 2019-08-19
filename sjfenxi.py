#数据分析
from htmlsoupClass import htmlsoup
from readexcle import readExcle
from collections import Counter
class sjfenxClass(object):
	
	def __init__(self, arg):
		super(sjfenxClass, self).__init__()
		self.arg = arg
		self.id1=arg
	#获取必发数据
	def _getbf(self):
		hs=htmlsoup(self.id1)
		bflist,bzbf,bflist_sjtd=hs.getbifa()
		return bflist,bzbf,bflist_sjtd
	def _getoz(self):
		hs=htmlsoup(self.id1)
		ozlist,bzoz=hs.getouzhi()
		return ozlist,bzoz
	def _getsc(self):
		hs=htmlsoup(self.id1)
		scblist,bzsc=hs.getsc()
		return scblist,bzsc

	#必发数据分析
	def bfsjfx(self):
		bflist,bzbf,bflist_sjtd=self._getbf()
		fxlist=[]
		#print(datelist)
		if bzbf==0:return fxlist,0
		for li in bflist:
			
			if int(li[1])==2:
				#print(li)
				if  float(li[12])<20:fxlist.append("必发平局分析：大冷")
				if  float(li[12])>=20 and float(li[12])<30 :fxlist.append("必发平局分析：过冷")
				if  float(li[12])>=30: fxlist.append("必发平局分析：热")
		#必发数据提点分析
		#print(bflist_sjtd[0][4].find("必发"))
		if bflist_sjtd[0][3].find("平局交易过冷")>=0:
			fxlist.append("数据提点分析：平局交易过冷")
		else:fxlist.append("数据提点分析：其他")
		print(fxlist)
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
	def bd(self):
		l1,bzbf=self.bfsjfx()
		l2,bzoz=self.ozsjfx()
		
		#l1=['必发平局分析：大冷', '数据提点分析：其他']
		#l2=['Iceland赔付正常', 'Iceland初返还高', 'Iceland负赔低-低于4']
			
		if bzbf*bzoz==0 or len(l2)*len(l1)==0:print("date lost ...");return 0
		print(l1)
		print(l2)

		df,l=readExcle('e:/05iceland.xlsx').read()
		x=0
		li=[]
		for i,row in df.iterrows():
			if row['ykzs']==l1[0] and row['kl']==l2[0] and row['peifu']==l2[1] and row['fupei']==l2[2] :
				x+=1
				#print(row['idnm'],row['jqc'],x)
				li.append(row['sg'])
			#print(row)
		res=Counter(li)
		scblist,bzsc=self._getsc()
		print(self.id1,res)


#j=sjfenxClass(854706)
#j.bd()
#print(j.ozsjfx())