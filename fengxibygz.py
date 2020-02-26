
#通过规则分析
#fengxibygz()
from zqconfigClass import zqconfigClass
from zqfenxi_gz import zqfenxi_gz
from tooth_excle import tooth_excleClass
import math
class fengxibygz(object):
	"""docstring for fengxibygz"""
	def __init__(self, arg):
		super(fengxibygz, self).__init__()
		self.arg = arg
		self.file1='e:/football/半球.csv'
		self.files2='e:/football/半球1213.xlsx'
	def __list_gz(self):
		list_gz103=['半球','规则1',	['count_len',0],['香港马会',11,12,31,32,101,102]]
		list_gz104=['半球','规则2',	['Bet365',11]]
		list_gz3=['半球','规则3',	['Bet365',31],['10BET',101]]
		list_gz=['半球','规则4',	['Bet365',32,101],['18Bet',102],['Sweden',102]]
		#'易胜博',['利记',102],['Sweden',102],['伟德',102],'威廉希尔',奥地利博彩,18Bet,香港马会,IFortuna.sk

		list_gz101=['半球','规则5',	['利记',32],['竞彩官方',31],['IFortuna.sk',32,101],['香港马会',11,12,31,32,101,102]]
		list_gz102=['半球','规则6',	['易胜博',32],['Iceland',102]]
		list_gz=list_gz103
		return list_gz
	def __get_df(self):
		df_idnm=zqconfigClass(0).select(self.file1)

		return df_idnm
	def __get_df_fromexcel(self):
		hh=tooth_excleClass(self.files2)
		df=hh.read()
		return df
	#对筛选的数据统计胜负结果
	def __count_sg(self,df):
		sg_list=list(df.sg.values)
		kk_df=zqfenxi_gz().count(sg_list)
		return kk_df
	#根据规则筛选数据
	def saixuan(self,df,gz):
		if len(gz)==0:
			print("规则错误09001")
			return 0
		if df.empty:
			print("数据集为空012001")
			return 0
		df_s=df
		bcgs=''
		print(gz)
		for gzrows in gz:

			bcgs=gzrows[0] #分开规则
			gzlist=gzrows[1:]
			cc='c_klmx_'+bcgs #构造列名，用于数据筛选
			colum_list=['count_len','count_re'] #冷热结果的特殊处理
			if bcgs in colum_list:cc=bcgs
			if bcgs=='Bet365':cc='c_klmx'

			df_s=df_s[ df_s[cc].isin(gzlist)] #数据集筛选，选出在列表中的数据
		return 1,df_s

	def t(self):

		gz=self.__list_gz()[2:]
		print(gz)
		b,df=self.saixuan(self.__get_df(),gz)
		print(df)
		print(self.__count_sg(df))
		return 0


k=fengxibygz(0)
k.t()		