

'''
	从网页获取数据
	主程序
'''
from savedateClass import savedateClass
from htmlsoupClass import htmlsoup
from zqconfigClass import zqconfigClass

import datetime
from pandas.core.frame import DataFrame
import pandas as pd

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
	def insert_none_bs(self,id1):
		print("无赛程")
		scberrorsql="insert into scb_error values (%s,%s)"
		liste=[]
		listee=[]
		liste.append(str(id1))
		liste.append("无赛程")
		listee.append(liste)
		dates=savedateClass()
		dates.insert(listee,scberrorsql)
		return 0
	#获取单场信息,并写入数据库
	def getbs(self,id1):
		print('开始获取',id1)
		dates=savedateClass()
		hs=htmlsoup(id1)

		scblist,bzsc,ozlist=hs.getscbandouzhi()

		#print(scblist)
		#return 0
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
		idlist=self._bsid_from_db(0,0,sql) #已有的比赛id
		#整理成List
		for idnmrow in idlist:
			for idnm0 in idnmrow:
				list1.append(idnm0)
		
		id_out_list=[] #获取还未进入数据库的比赛
		for x in range(idstart,idend+1):
			if x not in list1:
				id_out_list.append(x)#获取还未进入数据库的比赛
		iii=1
		id_in_list=[]	
		for id_out in id_out_list :
			if id_out in id_in_list:continue#增加如果是空值的简便处理方法
			if self.getbs(id_out):
				print ("-----获取比赛的数据成功-----")
				id_in_list.append(id_out)
				iii+=1
			else:
				id_in_list.append(id_out)
				for x in range(2,30,2):#增加如果是空值的简便处理方法
					id22=id_out+x
					if id22 in id_out_list:
						self.insert_none_bs(id22)#增加如果是空值的简便处理方法
						id_in_list.append(id22)
					iii+=1
					if iii>50:break
			if iii>50:break
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
		if idend is None:return 0
		if idend-idstart>500:
			idstart=idend-100
		#print("补齐之前比赛的数据{}-{}".format(idstart,idend))
		#print(minid[0][0],maxid[0][0])
		iii=1
		if idstart and idend:
			print("补齐比赛数据:{}{}赛季-->({}-{})<---".format(ls,nd,idstart,idend))
			iii=self.getbsid(idstart,idend)
			print('--->{}<---'.format(iii))
		return iii
	

	#获取要分析的比赛列表
	def get_id_list(self):
		h=zqconfigClass(0)
		df=h.select('zqconfig_bslb.csv')
		#print(df.idnm.values)
		return df
	
	#取网页数据返回Dataframe
	def get_ouzhi_df(self,idnm):
		k=htmlsoup(idnm)
		scblist,z,ouzhilist=k.getscbandouzhi()#赛程表和欧赔
		columns_list_ouzhi=['idnm', 'xh', 'bcgs', 'cz3', 'cz1', 'cz0', 'jz3', 'jz1', 'jz0', 'cgl3', 'cgl1', 'cgl0', 'jgl3', 'jgl1', 'jgl0', 'chf', 'jhf', 'ck3', 'ck1', 'ck0', 'jk3', 'jk1', 'jk0']
		df=DataFrame(ouzhilist,columns=columns_list_ouzhi)
		#df=df[df.bcgs.isin(['Expekt','BINGOAL','Sweden','Oddset','Iceland','Bet365','威廉希尔'])]
		#临时出入文件再读出
		df.to_csv('bifa.csv')
		df_ouzhi=zqconfigClass(0).select('bifa.csv')

		columns_list_scb=['idnm','zd','kd','nd','ls','lc','zjq','kjq','bssj']
		df2=DataFrame(scblist,columns=columns_list_scb)
		#临时出入文件再读出
		df2.to_csv('bifa.csv')
		df_scb=zqconfigClass(0).select('bifa.csv')
		#print(df_scb)
		return df_ouzhi,df_scb
	#取网页数据返回Dataframe
	def get_yapan_df(self,idnm):
		k=htmlsoup(idnm)
		yplist,z=k.getyapan()
		columns=['idnm','xh','bcgs','n1','jp','n2','n3','cp','n4']
		#print(yplist)
		df=DataFrame(yplist,columns=columns)
		df.to_csv('bifa.csv')

		df=zqconfigClass(0).select('bifa.csv')
		df1=df[df.bcgs=='Bet365']
		print(idnm,df1.jp.values)
		return 	df1
	#取网页数据返回Dataframe
	def get_bifa_df(self,idnm):
		k=htmlsoup(idnm)
		columns_list=['idnm', 'xh', 'xm', 'pl', 'gl', 'bd', 'bf', 'cjj', 'cjl', 'zjyk', 'bfzs', 'lrzs', 'ykzs']
		columns_sjtd=['idnm','ty','gm','fx','bz']
		listbifa,z,listsjtd=k.getbifa()

		df=DataFrame(listbifa,columns=columns_list)
		sjtd_df=DataFrame(listsjtd,columns=columns_sjtd)
	
		return df,z,sjtd_df
	

#存储策略	
class cl_save(getzqClass):
	#存入csv单场
	def to_csv_id(self,idnm):
		#存入临时文件
		path='e:/football/temp/'
		iiid=idnm
		#欧赔
		str1=str(iiid)+'scb.csv'
		str2=str(iiid)+'ouzhi.csv'
		df_ouzhi,df_scb=self.get_ouzhi_df(iiid)
		df_ouzhi.to_csv(path+str2)
		df_scb.to_csv(path+str1)
		#亚盘
		str3=str(iiid)+'yapan.csv'
		df_yapan=self.get_yapan_df(iiid)
		df_yapan.to_csv(path+str3)

		#必发
		str4=str(iiid)+'bifa.csv'
		str5=str(iiid)+'bifatd.csv'
		
		df_bifa,bz,sjtd_df=self.get_bifa_df(iiid)
		df_bifa.to_csv(path+str4)
		sjtd_df.to_csv(path+str5)
		return 0

	#批量存入未完场的比赛
	def to_csv(self):
		df=self.get_id_list()

		id_df=df[df['zt']=='未']
		print(id_df)
		id_li=id_df.idnm.values.tolist()
		
		#临时出入csv
		for iiid in id_li:
			print(iiid)
			#save to csv
			self.to_csv_id(iiid)
	
		return 0


	def from_csv(self,idnm):
		pass
	#存入db
	def to_db(self):
		df=self.get_id_list()

		id_df=df[df['zt']=='完']
		id_li=id_df.idnm.values.tolist()

		min_id=min(id_li)
		max_id=max(id_li)

		sql="select idnm from scb where idnm between " +str(min_id)+" and " +str(max_id)
		id_db_li=self._bsid_from_db(min_id,max_id,sql)
		for iiid in id_li:
			print(iiid)
			if iiid in id_db_li:
				continue
			#获取数据写入数据库
			#save_to_db

		return 0

	def from_db(self,idnm):
		pass

#获取数据策略
class zqfromdb:
	#获取
	#1、欧赔
	#2、亚盘
	#3、必发
	def __init__(self):
		self.path='e:/football/temp/'
		self.h=zqconfigClass(0)
	def from_csv_scb(self,idnm):
		files=self.path+str(idnm)+'scb.csv'
		#获取文件
		df=self.h.select(files)
		return df
	def from_csv_ouzhi(self,idnm):
		files=self.path+str(idnm)+'ouzhi.csv'
		#获取文件
		df=self.h.select(files)
		return df

	def from_csv_yapan(self,idnm):
		files=self.path+str(idnm)+'yapan.csv'
		#获取文件
		df=self.h.select(files)
		return df
	def from_csv_bifa(self,idnm):
		files=self.path+str(idnm)+'bifa.csv'
		#获取文件
		df=self.h.select(files)
		return df

	def from_csv_bifatd(self,idnm):
		files=self.path+str(idnm)+'bifatd.csv'
		#获取文件
		df=self.h.select(files)
		return df
	#生成单场ai数据 分步处理
	def ai_sj(self,scb,ouzhi,yapan,bifa,bifatd):
		ai_li=[]
		empty_df=DataFrame([[]])
		#-------------------------------------------
		#1\ai——scb处理
		#,idnm,zd,kd,nd,ls,lc,zjq,kjq,bssj
		if scb.empty:return empty_df
		li1=scb[['idnm','zd','kd','zjq','kjq']].values.tolist()[0]#第一行
		idnm=li1[0]
		#判断赛果
		if li1[-2]-li1[-1]>0:
			sg=3
		elif li1[-2]-li1[-1]==0:
			sg=1
		else:
			sg=0
		li1.append(sg)


		columns_scb=['idnm','zd','kd','zjq','kjq','sg'] #
		ai_scb_df=DataFrame([li1],columns=columns_scb)  #
		

		#------------------------------------------
		#2\yapan处理
		#     idnm  xh    bcgs     n1     jp    n2    n3  cp   n4
		if yapan.empty:return empty_df
		li1=yapan[['idnm','jp','n1','cp','n3']].values.tolist()[0]#第一行
	
		columns_scb=['idnm','jp','js1','cp','cs3'] #
		ai_yapan_df=DataFrame([li1],columns=columns_scb)  #

		##print(ai_yapan_df)

		#------------------------------------------
		#3\oz处理
		#['idnm' 'bcgs' 'cz3' 'cz1' 'cz0' 'jz3' 'jz1' 'jz0' .... 'chf' 'jhf' 'ck3' 'ck1' 'ck0' 'jk3' 'jk1' 'jk0']
		if ouzhi.empty:return empty_df
		columns=ouzhi.columns.values
		#print(columns)
		bcgs_li=['Bet365','Expekt','10BET','威廉希尔','Oddset','Iceland','Sweden']
		bc1='Bet365'
		col_365=['idnm','bcgs','cz3','cz1','cz0']  #---
		df=ouzhi[ouzhi.bcgs==bc1][col_365]
		if df.empty:return empty_df	

		oz_365=df.values.tolist()[0]			 	#----

		#计算凯利差 减赔付率
		df1=ouzhi[['idnm', 'bcgs','chf', 'jhf', 'ck3', 'ck1' ,'ck0']]
		columns_gz=['idnm', 'bcgs','chf', 'jhfc', 'ck3c', 'ck1c' ,'ck0c']#用于构造

		for bcc in bcgs_li:

			df=df1[df1.bcgs==bcc]
			columns2=[col+'_'+str(bcc) for col in columns_gz[2:]]
			
			if df.empty:
				li2=[0 for i in range(len(columns2))]#空
			else:
				li1=df.values.tolist()[0]
				
				jhfc=li1[3]-li1[2]
				ck3c=li1[4]*100-li1[2]
				ck1c=li1[5]*100-li1[2]
				ck0c=li1[6]*100-li1[2]
				
				li2=[li1[2],jhfc,ck3c,ck1c,ck0c]#

			col_365.extend(columns2)
			oz_365.extend(li2)
		ai_ouzhi_df=DataFrame([oz_365],columns=col_365)
		#print(ai_ouzhi_df)
		#------------------------------
		#4\bifa处理
		#idnm  xh   xm    pl    gl  bd  ...    cjj     cjl    zjyk  bfzs  lrzs  ykzs
		
		columns1=['lrzs','ykzs']
		li2=[]
		bf_columns=[]
		li2.append(idnm)
		bf_columns.append('idnm')
		ii=[1,2,3]
		#bifa=empty_df
		bifa_df=bifa[bifa.idnm==idnm]

		if bifa_df.empty:
			li3=[0 for i in range(len(columns1)*3)]
			for i in ii:
				col=[coo+str(i) for coo in columns1]
				bf_columns.extend(col)
			li2.extend(li3)
			
		else:
			
			for i in ii:
				bf=bifa_df[bifa_df.xh==i][columns1]
				col=[coo+str(i) for coo in columns1]
				li2.extend(bf.values.tolist()[0])
				bf_columns.extend(col)

		#  idnm    ty            gm                         fx    bz
		columns_td=['gm','fx']
		df=bifatd[bifatd.idnm==idnm][columns_td]
		if df.empty:
			li21=[0 for i in range(len(columns_td))]
		else:
			li21=df.values.tolist()[0]
		bf_columns.extend(columns_td)
		li2.extend(li21)

		ai_bf_df=DataFrame([li2],columns=bf_columns)
		#print(ai_bf_df)
		#----------------------------------------------
		#df_li=[ai_ouzhi_df,ai_yapan_df,ai_bf_df,ai_scb_df]
		df=pd.merge(ai_scb_df,ai_yapan_df,how='left',on='idnm')
		df=pd.merge(df,ai_ouzhi_df,how='left',on='idnm')
		df=pd.merge(df,ai_bf_df,how='left',on='idnm')

		#print(df.values.tolist())
		return df

	def from_db_ouzhi(self,idnm):
		pass
	def from_db_yapan(self,idnm):
		pass
	def from_db_bifa(self,idnm):
		pass

def test():
	h=zqfromdb()
	idnm=961683

	h.ai_sj(h.from_csv_scb(idnm),h.from_csv_ouzhi(idnm),h.from_csv_yapan(idnm),h.from_csv_bifa(idnm),h.from_csv_bifatd(idnm))
	#print(df)

	return 0
#主程序入口		
def main():
	cl=cl_save(0)
	#保存未完场数据
	#cl.to_csv()
	test()
	#完场数据写入数据 库


if __name__ == '__main__':
	main()
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

#h=getzqClass('').getbs(877543)
#print(h.bqbf(800355))

#补齐必发数据，没有必发数据时，加入必发数据
#h.bqbfmain(714214,714604)
#['k1联','19','783817','784031']
