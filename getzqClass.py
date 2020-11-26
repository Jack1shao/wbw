

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
import os
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



	#存入db
	#清理列表
	def qingli_lb(self):
		'''清理列表'''
		df=self.get_id_list()
		#获取已经完场的场次
		id_df=df[df['zt']=='完']
		id_li=id_df.idnm.values.tolist()

		#根据已知比赛场次寻找已在数据裤的场次
		list_idnm=self.getbsid_bylist(id_li)
		#二维转一维
		li_id=[]
		for li in list_idnm:
			for x in li:
				li_id.append(x)
		#2\数据库中没有的比赛id列表===z
		z=[id1 for id1 in id_li if id1 not in li_id]
		#
		df_notin=df[~df.idnm.isin(li_id)]
		#print(df_notin)
		files='zqconfig_bslb.csv'
		df_notin.to_csv(files)
		return z


	def to_db(self):
		df=self.get_id_list()
		#获取已经完场的场次
		id_df=df[df['zt']=='完']
		id_li=id_df.idnm.values.tolist()

		#1\获取数据库中批量比赛id

		#根据已知比赛场次寻找已在数据裤的场次
		list_idnm=self.getbsid_bylist(id_li)
		if list_idnm==0:return 0
		#二维转一维
		li_id=[]
		for li in list_idnm:
			for x in li:
				li_id.append(x)
		#2\数据库中没有的比赛id列表===z
		z=[id1 for id1 in id_li if id1 not in li_id]
		#
		#df_notin=df[~df.idnm.isin(li_id)]
		#print(df_notin)

		#3\存入数据库
		z1=z[:20] if len(z)>20 else z
		print('每次存入{}场比赛数据{}'.format(len(z1),z1))
		
		[getzqClass('').getbsid(idnm,idnm) for idnm in z1 if len(z1)>0 ]
		self.qingli_lb()
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
		columns_scb=['idnm','zd','kd','ls','lc','zjq','kjq'] 
		li1=scb[columns_scb].values.tolist()[0]#第一行
		idnm=li1[0]
		#判断赛果
		if li1[-2]-li1[-1]>0:
			sg=3
		elif li1[-2]-li1[-1]==0:
			sg=1
		else:
			sg=0
		li1.append(sg)

		columns_scb.append('sg')
		#
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
		bcgs_li=['Bet365','Expekt','威廉希尔','Oddset','Iceland','Sweden']
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
				
				jhfc=(li1[3]-li1[2])/li1[2]
				ck3c=(li1[4]*100-li1[2])/li1[2]
				ck1c=(li1[5]*100-li1[2])/li1[2]
				ck0c=(li1[6]*100-li1[2])/li1[2]
				
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
		
		bifa_df=bifa[bifa.idnm==idnm]
		#必发列项转行项
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

		#  idnm ty    gm    fx    bz
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

	def from_db_scb(self,idnm):
		'''时程表'''
		columns=['idnm','zd','kd','nd','ls','lc','zjq','kjq','bssj']
		sql="select s.* from scb s where s.idnm={}".format(idnm)
		
		scb_li=(savedateClass().select(sql))
		if len(columns)==len(scb_li[0]):
			scb_df=DataFrame(scb_li,columns=columns)
		else:
			scb_df=DataFrame([[]])

		print(scb_df)
		return scb_df
		
	def from_db_ouzhi(self,idnm):
		'''欧赔'''
		columns=['idnm','xh','bcgs','cz3','cz1','cz0','jz3','jz1','jz0',
		'cgl3','cgl1','cgl0','jgl3','jgl1','jgl0','chf','jhf','ck3','ck1','ck0','jk3','jk1','jk0']
		
		sql="select s.* from ouzhi s where s.idnm={}".format(idnm)
		
		dbsj_li=(savedateClass().select(sql))
		df=DataFrame(dbsj_li,columns=columns)


		#print(df)
		return df
		
	def from_db_yapan(self,idnm):
		'''亚盘'''
		columns=['idnm','xh','bcgs','n1','jp','n2','n3','cp','n4']
		
		sql="select s.* from yapan s where s.idnm={}".format(idnm)
		
		dbsj_li=(savedateClass().select(sql))

		if len(columns)==len(dbsj_li[0]):
			df=DataFrame(dbsj_li,columns=columns)
		else:
			df=DataFrame([[]])
		df2=(df[df.bcgs=='Bet365'])

		print(df2)
		return df2

	def from_db_bifa(self,idnm):
		'''必发'''
		columns=['idnm','xh','xm','pl','gl','bd','bf','cjj','cjl','zjyk','bfzs','lrzs','ykzs']
		
		sql="select s.* from bifa s where s.idnm={}".format(idnm)
		
		dbsj_li=(savedateClass().select(sql))
		df=DataFrame(dbsj_li,columns=columns)
		ii=[1,2,3]
		df=df[df.xh.isin(ii)]
		
		return df

	def from_db_bifatd(self,idnm):
		'''必发'''
		columns=['idnm','ty','gm','fx','bz']
		
		sql="select s.* from sjtdbf s where s.idnm={}".format(idnm)
		
		dbsj_li=(savedateClass().select(sql))
		df=DataFrame(dbsj_li,columns=columns)
		#print(df)

		return df
def save_tofiles_by_df(df,files1,mode):
	#files1=gu_jiekou_fuzhu().get_csvname(code)
	if df.empty:return 0
	if mode=='a' and os.path.exists(files1):
		df.to_csv(files1,mode='a',header=False)
		print('- 增量存入csv')
	else :
		df.to_csv(files1)
		print('- 覆盖存入csv')
	return 1	

def scaisj():
	h=zqfromdb()
	sql="select idnm,cp,jp from yapan where jp='半球' and ypgs='Bet365' "
	li=(savedateClass().select(sql))
	df=DataFrame(li,columns=['idnm','cp','jp'])
	#print(df)
	id_li=df.idnm.values.tolist()
	files1='e:/football/ai_zq_sj.csv'
	mode=''
	for idnm in id_li:
		df=h.ai_sj(h.from_db_scb(idnm),h.from_db_ouzhi(idnm),h.from_db_yapan(idnm),h.from_db_bifa(idnm),h.from_db_bifatd(idnm))
		
		if mode=='':
			mode='a' if os.path.exists(files1) else ''

		save_tofiles_by_df(df,files1,mode)
		

	return 0
def test():
	h=zqfromdb()
	kk=getzqClass(0)
	idnm=780898
	#df=h.from_db_bifa(idnm)
	#print(df)
	#csv取数
	#h.ai_sj(h.from_csv_scb(idnm),h.from_csv_ouzhi(idnm),h.from_csv_yapan(idnm),h.from_csv_bifa(idnm),h.from_csv_bifatd(idnm))
	#数据库取数
	df=h.ai_sj(h.from_db_scb(idnm),h.from_db_ouzhi(idnm),h.from_db_yapan(idnm),h.from_db_bifa(idnm),h.from_db_bifatd(idnm))
	print(df)
	return 0

#主程序入口		
def main():
	cl=cl_save(0)
	#1保存完场数据 #完场数据写入数据 库
	cl.to_db()

	#2保存未完场数据
	#cl.to_csv()

	#3生成ai数据
	#scaisj()

	#cl.from_csv_ouzhi()
	#df=cl.qingli_lb()
	#test()

if __name__ == '__main__':
	main()

#h=getzqClass('').idnm_in([])

#h=getzqClass('').getbs(877543)
#print(h.bqbf(800355))

#补齐必发数据，没有必发数据时，加入必发数据
#h.bqbfmain(714214,714604)
#['k1联','19','783817','784031']
