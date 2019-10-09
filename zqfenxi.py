#zqfenxi.py
from pandas.core.frame import DataFrame
from tooth_excle import tooth_excleClass
from collections import Counter
from zqconfigClass import zqconfigClass
from getjsbf import getjsbfClass
from zqfenxi_gz import zqfenxi_gz
import pandas as pd
import os
class zqfenxi(object):
	"""docstring for zqfenxi"""
	def __init__(self, arg):
		super(zqfenxi, self).__init__()
		self.arg = arg
		self.idnm=int(arg)
	"""
	#必发
	def bifa(self,df,idnm):
		kk=zqfenxi_gz()

		df1=df[df.idnm==idnm]
		li=[]
		for index,x in df1.iterrows():
			if len(li)>0:break
			li1=[]
			li1.append(x.idnm)
			mx_gl=kk.bifa_gl(x.glc3,x.glc1,x.glc0)
			li1.append(mx_gl)
			mx_yk=kk.bifa_ykzs(x.ykzs3,x.ykzs1,x.ykzs0)
			li1.append(mx_yk)
			li1.append('必发模型')
			#
			li.append(li1)
		return li
	def yapan_jcp(self,idnm):
		return 0

	#亚盘
	def yapan(self,df,idnm):

		kk=zqfenxi_gz()
		df_yapan=df[df.idnm==idnm]
		list_jp=[]
		list_cp=[]
		list_yp=[]
		for index,row in df_yapan.iterrows():
			if row.jp in list_jp or row.cp in list_cp:continue
			list_jp.append(row.jp)
			list_cp.append(row.cp)
		if len(list_jp)!=1:return list_yp#返回空
		list_yp.append(list_jp[0])
		list_yp.append(list_cp[0])
		list_yp.append(str(self.yapan_jcp(idnm)))
		#print(list_yp)
		return list_yp

	#欧指
	def ouzhi(self,df,idnm):
		kk=zqfenxi_gz()
		list_oz=kk.moxin_kaili(df,idnm)
		list_kong=['0',0,0,0,0,0,0]
		li=[]
		list11=[]
		for x in range(7):
			list11.append(list_kong)
		z=-1
		for x in list_oz:
			del x[0]
			x.pop(-1)
			if x[0]=='Iceland':	z=3
			if x[0]=='Oddset':	z=1
			if x[0]=='Expekt':	z=2
			if x[0]=='Sweden':	z=5
			if x[0]=='BINGOAL':	z=6
			if x[0]=='Bet365':z=0
			if x[0]=='威廉希尔':z=4
			if z!=-1:
				del list11[z]
				list11.insert(z,x)
		for x in list11:
			li.extend(x)
		return li
	#赛果
	def sg(self,df,idnm):
		kk=zqfenxi_gz()
		df1=df[df.idnm==idnm]
		li=[]
		for index,x in df1.iterrows():
			if len(li)>0:break
			li1=[]
			li1.append(x.idnm)
			li1.append(kk.sg_as(x.zjq-x.kjq))
			li1.append('赛果')
			#
			li.append(li1)
		return li

	#已有数据分析
	def fenxi_yysj(self):
		kk=zqfenxi_gz()
		df=tooth_excleClass('e:/0.5.xlsx').read()
		#按列值分组
		list_idnm=df.idnm.values
		id1_list=[]
		for x in list_idnm:
			if x not in id1_list:
				id1_list.append(x)
		fx_list=[]
		iii=0
		for idnm in id1_list:
			iii+=1
			#if iii>10:break
			li=[]
			#序号
			li.append(iii)
			#赛果
			list_sg=(self.sg(df,idnm))
			for x in list_sg:
				li.extend(x)
			#必发
			list_bifa=self.bifa(df,idnm)
			for x in list_bifa:
				li.extend(x)
			#欧赔
			list_ouzhi=self.ouzhi(df,idnm)
			for x in list_ouzhi:
				li.append(x)
		
			#亚盘
			list_yp=self.yapan(df,idnm)
			print(list_yp)
			for x in list_yp:
				li.append(x)

			print(len(li),li)
			fx_list.append(li)
		n=len(fx_list[0])
		columns1=[]
		for x in range(n):
			columns1.append('n'+str(x))
		print(n,columns1)
		df=DataFrame(fx_list,columns=columns1)
		df.to_csv('e:/555.csv',encoding="utf_8_sig")
		#print(fx_list)
		return df


	#构造规则方案配置表
	def fenxigzb_save(self):
		zy1='胜平多'
		zy2=' 平负'
		#li1=[['n37','11,11',zy1,'s2019091601'],['n9','11,11',zy1,'s2019091601']]
		#li1=[['n37','12',zy1,'s2019091602'],['n9','12',zy1,'s2019091602']]
		#li1=[['n37',11,zy1,'s2019091701'],['n23',11,zy1,'s2019091701']]
		li1=[['n39','1010',zy1,'s2019091702'],['n18','1010',zy1,'s2019091702']]
		df=DataFrame(li1,columns=['n','li','zy','name'])
		df.to_csv('zqconfig_gzb.csv',mode='a',header=False)
		print(df)
		return



	def fenxi4(self):
		df=zqconfigClass(0).select('e:/555.csv')
		df_dzb=zqconfigClass(0).select('zqconfig_gzb.csv')
		#规则方案名称列表
		#去重
		list111=set(df_dzb.name.tolist())
		print(list111)
		#遍历每个规则列表
		list_idnm=[]
		listsg=[]	
		for l in list111:
			#规则方案名称列表
			list222=df_dzb[df_dzb.name==l].values
			#传入数据表
			df1=df
			for x in list222:
				#规则
				li_mx=x[1].split(',')
				li_mx_new=[int(mx) for mx in li_mx]
				#筛选
				df1=df1[df1[x[0]].isin(li_mx_new)]
			list_idnm+=df1.n1.values.tolist()
			
			listsg=[]
			listsg+=df1.n2.values.tolist()
			print(list222,'------->',Counter(listsg))
		print(len(set(list_idnm)))
		return 0


	#未完成比赛数据
	def fenxi_wwbs(self):
		k=getjsbfClass(0)
		df=k.get_id_list()
		#idnm去重
		list_idnm=df.idnm.values
		id1_list=[]
		for x in list_idnm:
			if x not in id1_list:
				id1_list.append(x)

		fx_list=[]
		iii=0
		for idnm in id1_list:
			iii+=1

			#if iii>10:break
			li=[]
			#序号
			li.append(iii)

			#赛果
			li.extend([idnm,-1000,'赛果'])
			#必发
			df_bifa,z=k.get_bifa_df(idnm)#取网页
			if z!=0:
				list_bifa=(self.bifa(df_bifa,idnm))
			else: 
				#continue
				list_bifa=['0','0','0','0']
			
			[li.extend(x) for x in list_bifa]
			#欧赔
			df_ouzhi=k.get_ouzhi_df(idnm)#取网页
			list_oz=self.ouzhi(df_ouzhi,idnm)
			for x in list_oz:
				li.append(x)

			#亚盘
			df_yapan=k.get_yapan_df(idnm)#取网页
			list_yp=self.yapan(df_yapan,idnm)
			#li+=list_yp
			for x in list_yp:
				li.append(x)
			n=len(li)
			columns1=[]
			for x in range(n):
				columns1.append('n'+str(x))
			lili=[]
			lili.append(li)
			df=DataFrame(lili,columns=columns1)
			df.to_csv('e:/666.csv',mode='a',header=False,encoding="utf_8_sig")
			fx_list.append(li)

		n=len(fx_list[0])
		columns1=[]
		for x in range(n):
			columns1.append('n'+str(x))
		df=DataFrame(fx_list,columns=columns1)
		#df.to_csv('e:/666.csv',mode='a',header=False)
		return df


	#
	"""
	def  get_bisai_df(self):
		kk=zqconfigClass(0)
		df=kk.select('zqconfig_bslb.csv')
		print(df)
		return df
		
	#模型库，经人工赛选
	def read_mxk(self):
		files1='e:/mxk.xlsx'
		kk=tooth_excleClass(files1)
		df=kk.read()
		df=(df[df.xh15>0])#该值为手工填写
		df.to_csv('zqconfig_mxk.csv',encoding="utf_8_sig")
		return df
	#未完场数据模型
	def read_wwcsj_mx(self):
		files1='e:/666.csv'
		kk=zqconfigClass(0)
		df=kk.select(files1)
		print(df.head())
		return df

	#list去重
	def list_qc(self,list1):
		list_r=[]
		for x in list1:
			if x in list_r:
				continue
			list_r.append(x)
		list_r.sort()
		return list_r
	#计算离散度
	def jslsd(self,list_sg):
		kk=zqfenxi_gz()
		list_r=[]
		cc=kk.count(list_sg)
		lll=cc.values[0]
		li=[]
		li.append(lll[0]+lll[1])
		li.append(lll[2])
		li.append(lll[3])
		lsxi,fc=kk.lisan(li)
		list_r.extend(lll)
		list_r.append('-')
		list_r.extend(li)
		list_r.append(lsxi)
		list_r.append(fc)
		return list_r
	#计算各菠菜公司的离散度	
	def lsd_liebiao(self):
		list_mx=[31,32,11,12,101,102]
		list_yp=['球半', '半球', '两球', '一球', '受一球/球半', '一球', '平手/半球', '平手', '受半球/一球', '受球半', '受平手/半球', '受半球', '半球/一球', '受一球', '两球/两球半', '受两球', '球半/两球', '两球半', '受两球/两球半', '一球/球半', '三球/三球半', '三球', '受球半/两球', '两球半/三球', '受两球半', '三球半', '受两球半/三球']
		list_yp=self.list_qc(list_yp)
		print(list_yp)

		path_f='e:/csv/'
		uu=zqfenxi_gz()
		kk=zqconfigClass(0)
		list_files=os.listdir(path_f)
		#list_files=self.list_qc(list_files)
		list_f_in=[]
		for files in list_files:

			print(path_f+files)
			if files in list_f_in:continue
			list_f_in.append(files)
			df=kk.select(path_f+files)
			#生成模型
			df_mx=uu.get_mx(df)

			for yp in list_yp:
				list_to_csv=[]

				df=df_mx[df_mx.cp==yp]

				for x in list_mx:

					sss='c_klmx:{}'.format(x)
					df1=df[df.c_klmx==x]
					if df1.empty:
						print('kong')
						continue
					list_lsd=self.jslsd( list(df1.sg.values))
					print(list_lsd)
					if(list_lsd[9]==0.2):continue
					if list_lsd[5]+list_lsd[6]+list_lsd[7]<8:continue
					#[0, 0, 0, 1, '-', 0, 0, 1, 1.4142, 0.2]
					list_lsd.insert(0,sss)
					list_lsd.append(yp)
					list_lsd.append(files)
					list_to_csv.append(list_lsd)
					print(list_lsd)
				df=DataFrame(list_to_csv)
				df.to_csv('e:/mxk.csv',mode='a',header=False,encoding="utf_8_sig")
		return 0

	#建立筛选库--mx
	def creat_mxk(self,cp):
		#list_yp=['球半', '半球', '两球', '一球', '受一球/球半', '一球', '平手/半球', '平手', '受半球/一球', '受球半', '受平手/半球', '受半球', '半球/一球', '受一球', '两球/两球半', '受两球', '球半/两球', '两球半', '受两球/两球半', '一球/球半', '三球/三球半', '三球', '受球半/两球', '两球半/三球', '受两球半', '三球半', '受两球半/三球']
		list_yp=[]
		list_yp.append(cp)
		list_yp=self.list_qc(list_yp)

		df_r_mxk=self.read_mxk()
		path_f='e:/csv/'
		#print(df_r_mxk)
		uu=zqfenxi_gz()
		kk=zqconfigClass(0)

		for cp in list_yp:
			list_bcgs=self.list_qc(df_r_mxk[df_r_mxk.xh13==cp].xh14.values.tolist())
			print(cp,list_bcgs,len(list_bcgs))
		
			#以Bet365为基础
			df=kk.select(path_f+'Bet365.csv')
			#print(df.columns.values)
			df=df[df.cp==cp]
			df_mx3=uu.get_mx(df)
			print(df_mx3.head())
			print(len(df_mx3))

			for files in list_bcgs:
				if files=='Bet365.csv':continue
				print(files)
				df=kk.select(path_f+files)
				df=df[df.cp==cp]

				df_mx2=uu.get_mx(df)[['idnm','bcgs','c_klmx','c_zz','c_fh','j_klmx']]
				print(df_mx2.head())
				df_mx3=pd.merge(df_mx3,df_mx2,how='left',on='idnm')	
			files='e:/{}.csv'.format(cp.replace('/','-'))
			print(files)
			df_mx3.to_csv(files,encoding="utf_8_sig")
			#end for list_yp
		return 0

	def add_mxk_wwcsj(self):
		k=getjsbfClass(0)
		uu=zqfenxi_gz()
		df=k.get_id_list()
		list_idnm=self.list_qc(df.idnm.values.tolist())
		li=[]
		
		list_idnm.sort()
		print(list_idnm)
		df_mxk=self.read_mxk()
		files2='yhq_idnm_list.csv'
		df_idnm=zqconfigClass(0).select(files2)

		for idnm in list_idnm:
			li=[]
			df_idnm=zqconfigClass(0).select(files2)
			if df_idnm[df_idnm.idnm==idnm].empty==False:
				print('{}--已经生成模型--'.format(idnm))
				continue
			
			df_yapan=k.get_yapan_df(idnm)#亚盘
			if df_yapan.empty:continue#没有亚盘数据就跳过
			#获取初盘
			cp=df_yapan.cp.values.tolist()[0]
			#根据初盘从模型库中获取筛选出来的欧赔菠菜公司，并去重
			list_bcgs=self.list_qc(df_mxk[df_mxk.xh13==cp].xh14.values.tolist())
			#整理欧赔菠菜公司名称，去除(.csv)后缀
			bcgs=[]
			for b in list_bcgs:
				dd=b[:-4]
				bcgs.append(dd)
			bcgs.sort()#排序

			df_ouzhi,df_scb=k.get_ouzhi_df(idnm)#赛程和欧指
			df_bifa,z=k.get_bifa_df(idnm)#必发

			df_ouzhi=df_ouzhi[df_ouzhi.bcgs.isin(bcgs) ]

			df=df_scb[['idnm','zd','kd','zjq','kjq']]
			#merge，，拼接完整的数据集
			df=pd.merge(df,df_bifa,how='left',on='idnm')
			df=pd.merge(df,df_yapan[['idnm','jp','cp']],how='left',on='idnm')	
			df_q=pd.merge(df,df_ouzhi,how='left',on='idnm')	

			#生成模型1（Bet365）做为基础判断
			df_bet365=uu.get_mx(df_q[df_q.bcgs=='Bet365'])
			#循环
			for bcgs in bcgs:
				if bcgs=='Bet365':continue
				df_ddd=df_q[df_q.bcgs==bcgs]
				df_mx2=uu.get_mx(df_ddd)[['idnm','bcgs','c_klmx','c_zz','c_fh','j_klmx']]
				#拼接
				df_bet365=pd.merge(df_bet365,df_mx2,how='left',on='idnm')	

			files='e:/{}.csv'.format(cp.replace('/','-'))
			if os.path.exists(files):
				print('\n-->增加到{}'.format(files))
				df_bet365.to_csv(files,mode='a',header=False,encoding="utf_8_sig")
			else:
				print('无模型库文件，创建[{}]模型库'.format(cp))
				self.creat_mxk(cp)
				print('\n-->增加到{}'.format(files))
				df_bet365.to_csv(files,mode='a',header=False,encoding="utf_8_sig")

			files2='yhq_idnm_list.csv'
			list_111=[idnm,cp,df_scb.zd.values[0],df_scb.kd.values[0],df_scb.bssj.values[0]]
			df_idnm=DataFrame([list_111])
			df_idnm.to_csv(files2,mode='a',header=False,encoding="utf_8_sig")
		return 0


	
#获取完场数据
#h=zqfenxi(0).read_mxk()
#h=zqfenxi(0).fenxi_yysj()
#h=zqfenxi(0).creat_mxk('一球')

