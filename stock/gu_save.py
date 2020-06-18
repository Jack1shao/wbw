#gu_save
import tushare as ts
import datetime
import os
from pandas import read_csv
from pandas.core.frame import DataFrame

class gu_save(object):
	"""docstring for gu_save"""
	def __init__(self, arg):
		super(gu_save, self).__init__()
		self.arg = arg
		self.basc='basc'
		

	def get_csvmc(self,code):
		csv_path='d:/stock_csv/{}.csv'.format(code)
		return csv_path
	#股票基础数据1
	def get_base_from_api(self):
		
		list1=[]
		df = ts.get_stock_basics()
		max_timeToMarket=20200101
		for code,row in df.iterrows():
			#判断未上市的公司
			if row['timeToMarket']==0:
				list1.append(code)

		#删除未上市的公司记录
		df2=df.drop(list1,axis=0)
		return df2
	#股票基础数据2
	def get_base_from_db(self):
		files1=self.get_csvmc(self.basc)
		if os.path.exists(files1):
			with open(files1,'r',encoding='utf-8') as csv_file:
				df = read_csv(csv_file,index_col=0)#指定0列为index列
		return df
	#股票代码不起
	def getSixDigitalStockCode(self,code):
		strZero = ''
		for i in range(len(str(code)), 6):
			strZero += '0'
		return strZero + str(code)
	#	股票name
	def get_name(self,code1):
		df=self.get_base_from_db()
		#df=df[df.index==code]
		
		for code,row in df.iterrows():
			coo=self.getSixDigitalStockCode(code)
			
			if coo==code1:
				return row[0]
		print('未找到股票名字')	
		return ''
		#收索市值大小
	#市值，根据日线
	def get_sz(self,code1):
		df=self.get_k_from_csv(code1,'D')
		high=df[-1:].high.values.tolist()
		#print(high)
		df2=self.get_base_from_db()
		totals=df2.loc[int(code1)].totals
		sz=totals*high[0]
		#print(float('%.2f' % sz),'亿')#小数位数
		return float('%.2f' % sz)
	#上市时间
	def get_timeToMarket(self,code1):
	
		df2=self.get_base_from_db()
		time=df2.loc[int(code1)].timeToMarket
		return time

	#从接口取数
	def get_k_from_api(self,code1,ktype1):
		print('从api取-{0}-{1}'.format(code1,ktype1))
		code=str(code1)
		k_li=['m','w','D','30']
		if ktype1 not in k_li:
			print("k线类型错误")
			return 0
		if len(code)!=6:
			print("股票代码不是6位")
			return 0
		df=ts.get_k_data(code,ktype=ktype1)
		df['code']=str(code)
		df['ktype']=str(ktype1)
		gxrq = datetime.datetime.now().strftime('%Y-%m-%d')
		gxsj = datetime.datetime.now().strftime('%H%M')
		df['gxrq']=gxrq
		df['gxsj']=gxsj
		return df
	#从本地取数
	def get_k_from_csv(self,code,ktype1):
		print('从本地取-{0}-{1}'.format(code,ktype1))
		files1=self.get_csvmc(code+ktype1)
		if os.path.exists(files1):
			with open(files1,'r',encoding='utf-8') as csv_file:
				df = read_csv(csv_file,index_col=0)#指定0列为index列
		else:
			print('未找到股票数据，请先载入')
			return DataFrame([])
		return df
	#存入csv
	def save_k_to_csv(self,code,df,mode,ktype1):
		files1=self.get_csvmc(code+ktype1)
		if mode=='a':
			df.to_csv(files1,mode='a',header=False)
			print('- 增量存入csv')
		else :
			df.to_csv(files1)
			print('- 覆盖存入csv')
		return 1
	#通用
	def get_from_csv(self,files1):
	
		if os.path.exists(files1):
			with open(files1,'r',encoding='utf-8') as csv_file:
				df = read_csv(csv_file,index_col=0)#指定0列为index列
		return df
	#存入csv	
	def save_to_csv(self,code,df,mode):
		files1=self.get_csvmc(code)
		if mode=='a':
			df.to_csv(files1,mode='a',header=False)
			print('- 增量存入csv-{}'.format(files1))
		else :
			df.to_csv(files1)
			print('- 覆盖存入csv-{}'.format(files1))
		return 1

	#更新全部
	def pl_gx_all(self,ktype1):
		

		co_li=[]
		shou_fil=''
		files1=['sv_sz.csv','shou_m.csv','shou_w.csv','sv_dmd1.csv']

		if ktype1=='m':
			shou_fil=files1[0]
		if ktype1=='w':
			shou_fil=files1[1]
		
		if ktype1=='D':
			shou_fil=files1[2]
	
		shou_fil=files1[3]	
		code_li=self.get_from_csv( shou_fil).code.values.tolist()
		
		for code in code_li:
			co=self.getSixDigitalStockCode(code)
			co_li.append(co)
		self.pl_chunru(co_li,ktype1)
		return 1

	##去除St的股票和上市一年的股票
	def get_code_list(self):
		print('--去除St的股票和2019年后上市的股票--')
		df=self.get_base_from_db()
		n_li=[]
		for code,row in df.iterrows():
			if row[0].find('ST')<0 and row[14]<20190101:
				n_li.append(self.getSixDigitalStockCode(code))
		return n_li
	#去除St的股票和上市一年的股票的大名单
	def dmd1(self):
		li_df=[]
		n_li=self.get_code_list()
		for co in n_li:
			li_df.append([co,'除St的股票和2019年后大名单'])
		df=DataFrame(li_df,columns=[ 'code', 'name'])
		df.to_csv('sv_dmd1.csv')
		return 0

	#流通市值在50-2000亿
	def sz_50_2000(self):
		x1=50
		x2=2000
		code_li=self.get_from_csv('sv_dmd1.csv').code.values.tolist()
		co_li=[]
		for code in code_li:
			co=self.getSixDigitalStockCode(code)
			co_li.append(co)
		c_li=[]
		for code  in co_li:
			sz=self.get_sz(code)
			if sz>x1 and sz<x2:
				c_li.append([code,'市值在{0}-{1}之间'.format(x1,x2)])

		df=DataFrame(c_li,columns=[ 'code', 'name'])
		df.to_csv('sv_sz.csv')
		return 0
	#按列表批量存入数据
	def pl_chunru(self,list1,ktype1):
		if len(list1)==0:
			print('股票列表为ikon——pl_churu')
			return 0
		iii=0
		for code in list1:
			print('---{0}---{1}---'.format(iii,code))
			iii+=1
			df=self.get_k_from_api(code,ktype1)
			self.save_k_to_csv(code,df,'',ktype1)
		return 1

def main():
	print('	\n单独执行股票取数，开始...')
	kk=gu_save('0')

	ktype1=['30','D','w','m']
	i=0
	while i<10:
		i+=1
		print('0--获取所有 <30分钟K线>')
		print('1--获取所有 <日K线>')
		print('2--获取所有 <周K线>')
		print('3--获取所有 <月K线>')
		print('4--获取基础数据存入csv')
		print('91--大名单')
		print('92--市值在50-2000亿')
		print('93--热门')
		print('99--退出<99>')
		print('--')
		print('--')
		cc=input()
		if cc=='99':
			print('	退出<99>')
			break
		if cc=='91':
			kk.dmd1()
			print('---	91大名单---')
		if cc=='92':
			kk.sz_50_2000()
			print('---	92市值在50-2000亿---')
		n=int(cc)
		#print(cc,n)
		if n>len(ktype1):
			print('输入有误')
			continue
		if n==4:
			df=kk.get_base_from_api()
			kk.save_to_csv('basc',df,'')
			continue
		kk.pl_gx_all(ktype1[n])
		print('\n存入所有 <{}> K线 完毕\n'.format(ktype1[n]))
	print('程序完成，退出')	

if __name__ == '__main__':
	main()



