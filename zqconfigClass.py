#zqconfigClass.py

import os
from pandas.core.frame import DataFrame
from pandas import read_csv
import pandas as pd
class zqconfigClass(object):
	"""docstring for zqconfigClass"""
	def __init__(self, arg):
		super(zqconfigClass, self).__init__()
		self.arg = arg
		

	def cfg_save(self):
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
		df=DataFrame(between_list,columns=['ls','nd','id1','id2'])
		#df.rename()
		df.to_csv('zqconfig.csv')
		print(df)
		return 0
	def cfg_select(self):
		return self.select('zqconfig.csv')

	def save(self,df,files1):
		#files1='zqconfig_bslb.csv'
		if df.empty:
			print("empty")
			return 0
		df.to_csv(files1)
		return 1		
	def append(self,df,files1):
		df.to_csv(files1,mode='a',header=False)
		return 1	

	def select(self,files1):
		filepath_jcxx=files1
		#print("读取联赛配置文件，'*.csv'")
		if os.path.exists(files1):
			with open(files1,'r',encoding='utf-8') as csv_file:
				df = read_csv(csv_file,index_col=0)#指定0列为index列
		else:return DataFrame([])
		return df
	#队名对照表
	def cfg_dmdzb_save(self,df):
		listdzb=df.values
		if len(listdzb)==0:print('date is None');return 0
		#整理
		listzl=[]
		for li in listdzb:
			for x in range(0,4):
				
				if li[x]==li[x+4]:continue
				list11=[]
				list11.append(li[x])
				list11.append(li[x+4])
				list11.sort()
				if (list11 not in listzl):
					listzl.append(list11)
			
		listdzb3=[]
		while len(listzl)>0:
	
			listdzb2=[]
			for x in range(0,4):
				if len(listzl)==0:break
				i=listzl.pop();
				listdzb2.insert(x,i[0])
				listdzb2.insert(x+4,i[1])
			if len(listdzb2)!=8:
				l=int(len(listdzb2)/2)
				i=(4-l)
				
				for x in range(0,int(i)):
						listdzb2.insert(l+x,'0')
						listdzb2.insert(l+x+4,'0')
			if len(listdzb2)==8 :
				listdzb3.append(listdzb2)
		#list to datefame
		df=DataFrame(listdzb3,columns=['n1','n2','n3','n4','n5','n6','n7','n8'])
		df.to_csv('zqconfig_dmdzb.csv')
		print(df)
		return 0

	def cfg_dmdzb_append(self,df,files1):
		df.to_csv(files1,mode='a',header=False)
		return 0

	def cfg_dmdzb_select(self):
		df=self.select('zqconfig_dmdzb.csv')
		ii=0
		for index,x in df.iterrows():
			if x.n1==x.n5:
				ii+=1
				#print(x.n1)
			#if ii>10:self.cfg_save(df)

		return df
	#未完成的购买比赛列表
	def cfg_gmlb_save(self,df,files1):
		#files1='zqconfig_bslb.csv'
		if df.empty:
			print("empty")
			return 0
		df.to_csv('files1')
		return 1
	def cfg_gmlb_append(self,df,files1):
		df.to_csv(files1,mode='a',header=False)
		return 0
	def cfg_gmlb_select(self,files1):
		df=self.select(files1)
		return df
				

#zqconfigClass('').save(df1,files1)
#kk=zqconfigClass(0)
#if kk.arg==0:print(kk.cfg_dmdzb_select())
#kk.cfg_dmdzb_append(df,'zqconfig_dmdzb.csv')
#print(df.values)