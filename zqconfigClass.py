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
		filepath_jcxx='zqconfig.csv'
		print("读取联赛配置文件，'zqconfig.csv'")
		if os.path.exists(filepath_jcxx):
			with open(filepath_jcxx,'r',encoding='utf-8') as csv_file:
				df = read_csv(csv_file,index_col=0)#指定0列为index列
		else:return 0
		return df

zqconfigClass(''). cfg_select()
#zqconfigClass('').cfg_save()