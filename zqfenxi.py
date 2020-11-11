#zqfenxi.py
from pandas.core.frame import DataFrame
from tooth_excle import tooth_excleClass
from collections import Counter
from zqconfigClass import zqconfigClass
from getjsbf import getjsbfClass
from zqfenxi_gz import zqfenxi_gz
import pandas as pd
import os
import math
class zqfenxi(object):
	"""docstring for zqfenxi"""
	def __init__(self, arg):
		super(zqfenxi, self).__init__()
		self.arg = arg
		self.idnm=int(arg)
		self.files2='yhq_idnm_list.csv'#用于存放已经取数据的比赛信息
		self.files_mxk_lsd='e:/football/mxk.xlsx'#用于存放手工筛选的模型库的离散度

	def  get_bisai_df(self):
		kk=zqconfigClass(0)
		df=kk.select('zqconfig_bslb.csv')
		print(df)
		return df
		
	#模型库，经人工赛选
	def read_mxk(self):
		
		kk=tooth_excleClass(self.files_mxk_lsd)
		df=kk.read()
		df=(df[df.xh15>0])#该值为手工填写
		df.to_csv('zqconfig_mxk.csv',encoding="utf_8_sig")
		return df
	#已有数据分析
	'''def fenxi_yysj(self):
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
				'''
	#未完场数据模型
	'''	def read_wwcsj_mx(self):
		files1='e:/666.csv'
		kk=zqconfigClass(0)
		df=kk.select(files1)
		print(df.head())
		return df'''

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
	#计算各菠菜公司的离散度,生产模型库MXK.CSV	
	def lsd_liebiao(self):
		list_mx=[31,32,11,12,101,102]
		list_yp=['球半', '半球', '两球', '一球', '受一球/球半', '一球', '平手/半球', '平手', '受半球/一球', '受球半', '受平手/半球', '受半球', '半球/一球', '受一球', '两球/两球半', '受两球', '球半/两球', '两球半', '受两球/两球半', '一球/球半', '三球/三球半', '三球', '受球半/两球', '两球半/三球', '受两球半', '三球半', '受两球半/三球']
		list_yp=self.list_qc(list_yp)
		print(list_yp)

		path_f='e:/football/csv/'
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

					df1=df[df.c_klmx==x]
					if df1.empty:
						print('kong')
						continue
					list_lsd=self.jslsd( list(df1.sg.values))
					print(list_lsd)
					if(list_lsd[9]==0.2):continue
					if list_lsd[5]+list_lsd[6]+list_lsd[7]<8:continue
					#[0, 0, 0, 1, '-', 0, 0, 1, 1.4142, 0.2]
					list_lsd.insert(0,x)
					list_lsd.append(yp)
					list_lsd.append(files)
					list_to_csv.append(list_lsd)
					print(list_lsd)
				df=DataFrame(list_to_csv)
				df.to_csv('e:/football/mxk.csv',mode='a',header=False,encoding="utf_8_sig")
		return 0

	#建立筛选库--mx
	def creat_mxk(self,cp):
		#list_yp=['球半', '半球', '两球', '一球', '受一球/球半', '一球', '平手/半球', '平手', '受半球/一球', '受球半', '受平手/半球', '受半球', '半球/一球', '受一球', '两球/两球半', '受两球', '球半/两球', '两球半', '受两球/两球半', '一球/球半', '三球/三球半', '三球', '受球半/两球', '两球半/三球', '受两球半', '三球半', '受两球半/三球']
		list_yp=[]
		list_yp.append(cp)
		list_yp=self.list_qc(list_yp)

		df_r_mxk=self.read_mxk()
		path_f='e:/football/csv/'
		#print(df_r_mxk)
		uu=zqfenxi_gz()
		kk=zqconfigClass(0)

		for cp in list_yp:
			#获取需要的菠菜公司并去重
			list_bcgs=self.list_qc(df_r_mxk[df_r_mxk.xh13==cp].xh14.values.tolist())
			print(cp,list_bcgs,len(list_bcgs))
		
			#以Bet365为基础
			df=kk.select(path_f+'Bet365.csv')
			#print(df.columns.values)
			df=df[df.cp==cp]

			#bet365的欧洲指数
			df_ouzhi2=df[['idnm','cz3','cz1','cz0']]
		
			
			df_mx3=uu.get_mx(df)[['idnm','zd','kd','sg','jp','cp','c_klmx','c_zz','c_fh']]
			#print(df_mx3.columns.values)
			#['idnm' 'zd' 'kd' 'sg' 'jp' 'cp' 'bfgl' 'ykzs' 'bcgs' 'c_klmx' 'c_zz' 'c_fh' 'j_klmx' 'j_zz' 'j_fh']
			
			print(df_mx3.head())
			#print(len(df_mx3))
			#return 0
			#再次读取模型库
			iii_lr=0

			for files in list_bcgs:
				if files=='Bet365.csv':continue
				print(files)
				#读取数据文件.csv
				df=kk.select(path_f+files)
				df=df[df.cp==cp]
				#模型库数据

				#生成模型
				df_mx21=uu.get_mx(df)[['idnm','bcgs','c_klmx','c_zz','c_fh','j_klmx']]
				print(df_mx21.head())
				#再次读模型库，为添加冷热情况
				
				df_mxk=self.read_mxk()
				df_mxk_lr=df_mxk[(df_mxk.xh13==cp)&(df_mxk.xh14==files)]
				#增加模型库的信息
				df_mx2=pd.merge(df_mx21,df_mxk_lr,how='left',left_on='c_klmx',right_on='xh2')	
				#df_mx2=df_mx2[['idnm','bcgs','c_klmx','xh15','c_fh','j_klmx']]
				df_mx2=df_mx2[['idnm','bcgs','c_klmx','c_fh','c_zz']]
				bcgsss=df_mx2.iloc[0,1]
				print(bcgsss)
				#df_mx2.rename(columns={'xh15':'lenre_{}'.format(bcgsss)},inplace = True)
				df_mx2.rename(columns={'c_klmx':'{}c_klmx'.format(bcgsss)},inplace = True)
				df_mx2.rename(columns={'c_fh':'{}c_fh'.format(bcgsss)},inplace = True)
				df_mx2.rename(columns={'c_zz':'{}c_zz'.format(bcgsss)},inplace = True)
				df_mx2.rename(columns={'bcgs':'{}bcgs'.format(bcgsss)},inplace = True)
				#合并模型
				df_mx3=pd.merge(df_mx3,df_mx2,how='left',on='idnm')	
			#增加一列冷热情况，个位为冷的数量，百位为热的数量
			list_lr=[]
			for index,row in df_mx3.iterrows():
				lr=[]
				lr.append(row.idnm)
				i2=row.values.tolist().count(2345)
				i1=row.values.tolist().count(1234)
				ii=i2*100+i1
				lr.append(i2)
				lr.append(i1)
				list_lr.append(lr)
			#print(list_lr)
			df_lr=pd.DataFrame(list_lr,columns=['idnm','count_len','count_re'])
			#print(df_lr)
			df_mx3=pd.merge(df_mx3,df_ouzhi2,how='left',on='idnm')
			ccc=df_mx3.columns.values.tolist()
			vvv=df_mx3.values.tolist()

					
			files='e:/football/{}1.csv'.format(cp.replace('/','-'))
			print(files)
			df_mx3.to_csv(files,encoding="utf_8_sig")
			#end for list_yp
		return 0
	#未完场比赛数据获取和建立模型。
	def add_mxk_wwcsj(self):
		k=getjsbfClass(0)
		uu=zqfenxi_gz()
		#未完成比赛idnm
		df=k.get_id_list()
		list_idnm=self.list_qc(df.idnm.values.tolist())
			
		print(list_idnm)
		df_mxk=self.read_mxk()
		#print(df_mxk)
		files2='yhq_idnm_list.csv'
		df_idnm=zqconfigClass(0).select(files2)

		for idnm in list_idnm:
			df_idnm=zqconfigClass(0).select(files2)
			if df_idnm[df_idnm.idnm==idnm].empty==False:
				print('{}--已经生成模型--'.format(idnm))
				continue
			
			df_yapan=k.get_yapan_df(idnm)#亚盘
			if df_yapan.empty:continue#没有亚盘数据就跳过
			#获取初盘
			cp=df_yapan.cp.values.tolist()[0]
			#根据初盘从模型库中获取筛选出来的欧赔菠菜公司，并去重
			if cp not in ['半球','受半球']:print('---非非非半球---',cp);continue
			list_bcgs=self.list_qc(df_mxk[df_mxk.xh13==cp].xh14.values.tolist())
			#整理欧赔菠菜公司名称，去除(.csv)后缀
			list_bcgs2=[]
			list_bcgs2.append('Bet365')#保证有'Bet365'
			for b in list_bcgs:
				dd=b[:-4]
				list_bcgs2.append(dd)
			list_bcgs2.sort()#排序
			
			df_ouzhi,df_scb=k.get_ouzhi_df(idnm)#赛程和欧指
			df_bifa,z=k.get_bifa_df(idnm)#必发

			df_ouzhi=df_ouzhi[df_ouzhi.bcgs.isin(list_bcgs2) ]

			df=df_scb[['idnm','zd','kd','zjq','kjq']]
			#merge，，拼接完整的数据集
			df=pd.merge(df,df_bifa,how='left',on='idnm')
			df=pd.merge(df,df_yapan[['idnm','jp','cp']],how='left',on='idnm')
			df_q=pd.merge(df,df_ouzhi,how='left',on='idnm')

			#生成模型1（Bet365）做为基础判断
			df_bet365=uu.get_mx(df_q[df_q.bcgs=='Bet365'])
			df_bet365['sg']=-1000
			#循环
			iii_len=0
			iii_re=0
			for bcgs in list_bcgs2:
				if bcgs=='Bet365':continue
				df_ddd=df_q[df_q.bcgs==bcgs]
				print('取模型',bcgs)
				df_mx2=uu.get_mx(df_ddd)[['idnm','bcgs','c_klmx','c_zz','c_fh','j_klmx']]
				#取单值,判断在模型库中的情况
				if df_mx2.empty:
					print('empty--')
				else:
					if df_mx2.loc[0,'bcgs']==None:
						print('{}不存在'.format(bcgs))
					else:
						bcgs_csv="{}.csv".format(df_mx2.loc[0,'bcgs'])
						c_klmx_1=df_mx2.loc[0,'c_klmx']
						print(bcgs_csv,c_klmx_1)
						df_mxk=self.read_mxk()
						df_mxk2=df_mxk[(df_mxk.xh2==c_klmx_1)&(df_mxk.xh13==cp)&(df_mxk.xh14==bcgs_csv)]
						print('mxk:',df_mxk2)
					if df_mxk2.empty:
						df_mx2['c_zz']=-1
					else:
						d_index = list(df_mxk2.columns).index('xh15')
						df_mx2['c_zz']=df_mxk2.iloc[0,d_index]
						if df_mxk2.iloc[0,d_index]==2345:iii_len+=1
						if df_mxk2.iloc[0,d_index]==1234:iii_re+=1

				#拼接
				df_bet365=pd.merge(df_bet365,df_mx2,how='left',on='idnm')	
			#增加一列冷热情况，个位为冷的数量，百位为热的数量
			df_bet365['count_len']=iii_len
			df_bet365['count_re']=iii_re
			print(df_bet365)
			files='e:/football/{}.csv'.format(cp.replace('/','-'))
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
	def get_yjmx_idnm_list(self):
		files2='yhq_idnm_list.csv'
		
		df_idnm=zqconfigClass(0).select(files2)
		df=df_idnm.sort_values(by=['cp','bssj'],axis = 0,ascending = True)
		print(df)
		df=df_idnm.sort_values(by=['bssj','cp'],axis = 0,ascending = True)
		print(df)
		return df

class gu_getfromdb(object):
	"""获取本地数据"""
	#获取本地文件数据
	def get_fromfiles(self,files1):
		
		print('来自{1}类--从本地文件{0}取数--'.format(files1,self.__class__.__name__))
		
		if os.path.exists(files1):
			with open(files1,'r',encoding='utf-8') as csv_file:
				df = pd.read_csv(csv_file,index_col=0,keep_default_na=False)#指定0列为index列
		else:
			print('未找到数据，请先载入')
			return DataFrame([])
		return df
#获取完场数据
#h=zqfenxi(0).read_mxk()
#h=zqfenxi(0).fenxi_yysj()

#生成模型库，mxk.csv
#h=zqfenxi(0).lsd_liebiao()

#根据模型库，生成单个分析文件
#h=zqfenxi(0).creat_mxk('半球')
def test():
	gg=gu_getfromdb()
	cp='半球'
	files1='e:/football/{}1.csv'.format(cp)
	df=gg.get_fromfiles(files1)
	ccc=df.columns.values.tolist()
	vvv=df.values.tolist()
	for row in vvv:
		for i in range(0,len(row)):
			if row[i] is '':
				row[i]=0
		#print(row)
	df=DataFrame(vvv,columns=ccc)		
	print(df.head())
	print(df.shape())
	files='e:/football/{}2.csv'.format(cp.replace('/','-'))
	print(files)
	df.to_csv(files,encoding="utf_8_sig")
	return 0
def main():
	gg=gu_getfromdb()
	cp='半球'
	files1='e:/football/{}1.csv'.format(cp)
	data=gg.get_fromfiles(files1)
	print(data.head())
	print(data.shape)
	data_train, data_test= train_test_split(data,test_size=0.1, random_state=0)
	print ("训练集统计描述：\n",data_train.describe().round(2))
	print ("验证集统计描述：\n",data_test.describe().round(2))
	print ("训练集信息：\n",data_train.iloc[:,2].value_counts())  
	print ("验证集信息：\n",data_test.iloc[:,2].value_counts())   

	X_train=data_train.iloc[:,4:10]#  data_train.iloc[:,0:-2]     
	X_test=data_test.iloc[:,4:10] #data_train.iloc[:,0:-2]
	feature=data_train.iloc[:,4:10].columns
	print (feature)
	return 0

if __name__ == '__main__':
	h=zqfenxi(0).creat_mxk('半球')
	#main()

