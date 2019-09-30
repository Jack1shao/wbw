#zqfenxi.py
from pandas.core.frame import DataFrame
from tooth_excle import tooth_excleClass
from collections import Counter
from zqconfigClass import zqconfigClass
from getjsbf import getjsbfClass
from zqfenxi_gz import zqfenxi_gz
class zqfenxi(object):
	"""docstring for zqfenxi"""
	def __init__(self, arg):
		super(zqfenxi, self).__init__()
		self.arg = arg
		self.idnm=int(arg)
	
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

	def fenxi2(self):
		df=zqconfigClass(0).select('e:/555.csv')
		return 0
	def get_bisai_df(self):
		k=getjsbfClass(0)
		df=k.get_id_list()
		print(df)
		return
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

#获取完场数据
#h=zqfenxi(0).main()
#h=zqfenxi(0).fenxi_yysj()

