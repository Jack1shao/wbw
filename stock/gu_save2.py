'''获取数据'''
import tushare as ts
import datetime
import os
from pandas import read_csv
from pandas.core.frame import DataFrame
from collections import namedtuple

#
path='d:/stock_csv/'
basc_file=path+'basc.csv'
fqyz_file=path+'fqyz.csv'

Stock=namedtuple('Stock','code name hangye totals files1')
ts.set_token('4d4e8c66f3fe804a585a345419362a9982790682a79ef65214b5d5e1')
#数据获取接口
class gu_getfromapi:
	'''从api获取数据'''
	#获取api 数据
	def api_D_k(self,code1,start_day):
		
		'''新的接口Pro'''
		pro = ts.pro_api()
		#日期处理
		rq_now = datetime.datetime.now().strftime('%Y%m%d')
		rq_kaishi='20140103'
		start_d=rq_kaishi if start_day=='' else start_day
		#获取数据
		df=pro.daily(ts_code=code1, start_date=start_d, end_date=rq_now)
		df.rename(columns={'vol':'volume','trade_date':'date','ts_code':'code'}, inplace=True) 
		df=df.sort_values(by='date' , ascending=True)
		return df

	#全天模式
	def api_allday_k(self,date1):
		df = pro.daily(trade_date=date1)
		return df
	#获取基础数据api
	def api_base(self):
		df = ts.get_stock_basics()
		rq_now = datetime.datetime.now().strftime('%Y%m%d')
		df['gxrq']=rq_now

		return df

class gu_getfromdb(object):
	"""获取本地数据"""
	#获取本地文件数据
	def get_fromfiles(self,files1):
		
		print('来自{1}类--从本地文件{0}取数--'.format(files1,self.__class__.__name__))
		
		if os.path.exists(files1):
			with open(files1,'r',encoding='utf-8') as csv_file:
				df = read_csv(csv_file,index_col=0)#指定0列为index列
		else:
			print('未找到数据，请先载入')
			return DataFrame([])
		return df
		

#数据存储接口
class gu_save:
	#存入数据
	def save_to_db(self,df,type1):
		return 0
	#存入csv
	def save_tofiles_by_df(self,df,files1,mode):
		#files1=gu_jiekou_fuzhu().get_csvname(code)
		if df.empty:return 0
		if mode=='a' and os.path.exists(files1):
			df.to_csv(files1,mode='a',header=False)
			print('- 增量存入csv')
		else :
			df.to_csv(files1)
			print('- 覆盖存入csv')
		return 1
#辅助功能
class gu_fuzhu:

	#代码补全处理
	def code_buquan(self,code):

		strZero = ''
		for i in range(len(str(code)), 6):
			strZero += '0'

		code1=strZero + str(code)
		if code1[0]=='6':
			code2=code1+'.SH'
		else:
			code2=code1+'.SZ'
		return code2
	#
	def get_csvname(self,code):
		if code=='basc':
			csv_path=path+'{}.csv'.format(code)
		else:	
			co=self.code_buquan(code)
			csv_path=path+'{}.csv'.format(co)
		return csv_path

	#计算复权因子
	def get_fuquanyinzhi(self,code):

		return 0


#策略
#策略1存入csv
#策略2存入db
#策略3获取新api增量数据
#策略4获取旧api
#策略5获取本地from db
#策略6获取本地from csv

#功能策略
class gongnengchelv(gu_getfromapi,gu_save,gu_getfromdb):
	#存储基础数据
	def savebasc(self):
		'''存储基础数据'''
		print('存储基础数据')
		code1='basc'
		files1=gu_fuzhu().get_csvname(code1)
		mode=''
		df=self.api_base()
		bb=self.save_tofiles_by_df(df,files1,mode)
		return bb
	#获取全部代码列表，代码未补全
	def get_allcode(self):

		df=self.get_fromfiles(basc_file)
		code_li=df.index.values.tolist()
		code_li.sort()
		return code_li
	#K线增量存储
	def D_k_add(self,code1):
		#code1='600609'
		files1=gu_fuzhu().get_csvname(code1)
		jyrl_filse='d:/stock_csv/jyrl.csv'
		#文件存在，则为增量 修改模式
		mode='a' if os.path.exists(files1) else ''
		md='a' if os.path.exists(jyrl_filse) else ''
		#mode='a'
		if mode=='a':
			df1=self.get_fromfiles(files1)#获取本地df
			date_li=df1.date.values.tolist()#日期列
			date_max=max(date_li)#最大日期
			#获取交易日历，如果最大值与日历相等，返回，不取数
			if md=='a':
				jyrl_df=self.get_fromfiles(jyrl_filse)
				jyrl_li=jyrl_df.date.values.tolist()
				rl_max=max(jyrl_li)
				print(rl_max,date_max)
				if date_max==rl_max:
					print('最新数据')
					return 2
			start_d=str(date_max+1)
		else:
			start_d='20000101'
		#获取api ‘D’ k线
		df=self.api_D_k(gu_fuzhu().code_buquan(code1),start_d)
			#转为字符串
	
		if df.empty:
			print('增量为空Df 00001')
			return 1
		else:
			self.save_tofiles_by_df(df,files1,mode)
			return 0
	#单日全量存储
	def D_k_add_oneday(self,date):
		#数据存在，存入文件，并添加交易日历

		#文件存在，则添加

		pass
	#获取交易日历
	def jiaoyirili(self):
	 	'''根据5只代表票获得交易日历'''
	 	code5_li=['000002','000001','600006','600609','600000']
	 	files1='d:/stock_csv/jyrl.csv'
	 	mode='a' if os.path.exists(files1) else ''
	 	print('获得交易日历--开始--')
	 	if mode=='a':
	 		df=self.get_fromfiles(files1)
	 		rl_li=df.date.values.tolist()
	 		rl_max=max(rl_li)
	 	else:
	 		rl_li=[]
	 		rl_max='20000101'
	 	rl_li2=[]
	 	for co in code5_li:
	 		co_files=gu_fuzhu().get_csvname(co)
	 		df=self.api_D_k(gu_fuzhu().code_buquan(co),rl_max+1)
	 		date_li=df.date.values.tolist()
	 		for dd in date_li:
	 			if dd in rl_li or dd in rl_li2:
	 				continue
	 			else:
	 				rl_li2.append(dd)
	 	rl_li2.sort()
	 
	 	jyrl_li=[]
	 	for rl in rl_li2:
	 		jyrl_li.append([rl])
	 		print(rl)

	 	jyrl_df=DataFrame(jyrl_li,columns=['date'])
	 	jyrl_df.sort_values(by='date' , ascending=True)
	 	#print(jyrl_df)
	 	self.save_tofiles_by_df(jyrl_df,files1,mode)
	 	print('获得交易日历--结束--')
	 	return 0
	#从基础数据中获取code列表，并遍历获取api数据,本功能可以再次继承
	#可单独写入策略
	def qlzj(self):
		#获取全部列表
		code_li=self.get_allcode()
		ii=0#辅助打印，用于查看进度
		for co in code_li:
			#if int(co)<603131:continue
			print(co,ii)
			self.D_k_add(co)
			ii+=1

		return 0
#生成复权数据 
class fq(gu_save,gu_getfromdb):
	'''生成复权数据'''
	#复权因子
	def fqyz(self,code1):
		'''计算新复权因子'''
		
		files1=gu_fuzhu().get_csvname(code1)
		code_bq=gu_fuzhu().code_buquan(code1)
		#获取单个票数据
		df=self.get_fromfiles(files1)
		#转换为np
		values_df=df.values
		#提前复权因子 存入fqyz_li； for语句
		fqyz_li=[]
		close_bz=0#标志位
		for vv in values_df:
			
			if close_bz==0:
				close_bz=vv[5]
				continue

			if vv[6]!=close_bz:
				#print(code_bq,vv[1],vv[5],vv[6],close_bz,close_bz-vv[6])
				fqyz_li.append([code_bq,vv[1],close_bz-vv[6]])
			close_bz=vv[5]
		
		columns_fqyz=['code','date','fqyz_zh']
		df=DataFrame(fqyz_li,columns=columns_fqyz)
		return df
	#增加复权因子存入文件	
	def fqyz_add(self,df):
		files_fqyz=fqyz_file#全局变量复权因子文件
		mode='a' if os.path.exists(files_fqyz) else ''
		code1=df.code.values[0]
	
		if mode=='a':
			df_fqyz=self.get_fromfiles(files_fqyz)
			df_fqyz=df_fqyz[df_fqyz.code==code1]
			
			#已经存在的列表
			date_li=df_fqyz.date.values.tolist()
			#不存在的数据
			df_in=df[~(df.date.isin(date_li))]
			
			if df_in.empty:
				print('复权因子无增加')
				return 1
			else:
				self.save_tofiles_by_df(df_in,files_fqyz,mode)	
				return 0	
		#全量增加
		print("全量增加复权因子存入文件{}".format)
		self.save_tofiles_by_df(df,files_fqyz,mode)	

		return 0
	'''获取已经计算好的复权因子'''	
	def get_fqyz(self,code1):
		'''获取已经计算好的复权因子'''
		files_fqyz=fqyz_file
		df_fqyz=self.get_fromfiles(files_fqyz)
		code_st=gu_fuzhu().code_buquan(code1)

		df_fqyz=df_fqyz[df_fqyz.code==code_st]
		return df_fqyz

	#前复权
	def qfq(self,code1):
		'''前复权'''
		files1=gu_fuzhu().get_csvname(code1)
		df_fqyz=self.get_fqyz(code1)
		print(df_fqyz)
		#文件存在，则为增量 修改模式
		mode='a' if os.path.exists(files1) else ''
		#mode='a'
		if mode=='':
			print('无数据')
			return -1

		df1=self.get_fromfiles(files1)#获取本地df
		#按时间排序
		df=df1.sort_values(by='date' , ascending=True)
		print(df.head())
		columns1=df.columns.values.tolist()
		gu_li=df.values
		#print(gu_li)
		ln=len(df1)
		
		for i in range(ln,0,-1):
			ii=i-1
			#print(ii,gu_li[ii])
			##print(i,df['date'])
		pass
	#后复权
	def hfq(self,code1):

		pass

def test():
	g=gongnengchelv()

	code1='300568'
	#1、增量获取k线
	#g.D_k_add(code1)

	#2、获取交易日历
	#g.jiaoyirili()
	#3、获取日线
	#g.qlzj()

	#4、生产复权数据
	f=fq()
	#复权因子增加
	#df=f.fqyz(code1)
	#f.fqyz_add(df)
	#计算前复权
	f.qfq(code1)
	return 0
def main():

	code5_li=['000002','000001','600006','600609','600000']
	g=gongnengchelv()
	#1、获取基础数据#getbasc
	g.savebasc()
	#2、获取交易日历（ ['000002'，'000001'，'600006'，'600609'，'600000']）
	for co in code5_li:
		print(co)
		g.D_k_add(co)
	
	g.jiaoyirili()
	#3、从allday增加数据
	#3、从基础数据中获取code列表，并遍历获取api数据
	#g.qlzj()

	#获取复权因子
	#生产复权k线


if __name__ == '__main__':
	#输入股票代码获取该代码的基础信息
	#print(gu_save.__doc__)
	test()
	#main()
	#code1='300568'
	#fq().fqyz(code1)
	#code1='300568'
	#t().savebasc()
	#t().D_k_add(code1)
	#df=gs.api_base_from_api()
	#print(df.head(),len(df))
	#print(gu_jiekou_fuzhu().get_csvname('002498'))

