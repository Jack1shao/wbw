import os
from pandas import read_csv
from collections import namedtuple
from pandas.core.frame import DataFrame
import csv
Stock=namedtuple('Stock','xh code name cl clname')
class file_op:
	#'''--file_op类--通用--读取文件'''
	def get_from_csv(self,files1):
	
		if os.path.exists(files1):
			with open(files1,'r',encoding='utf-8') as csv_file:
				df = read_csv(csv_file,index_col=0)#指定0列为index列
		return df
	#读取文本文件to Df
	def get_txt(self,files1):
		st_li=[]
		if os.path.exists(files1):
			with open(files1,'r',encoding='utf-8') as csv_file:
				df = read_csv(csv_file,index_col=0)#指定0列为index列
				columns=df.columns

			with open(files1,'r',encoding='utf-8') as csv_file:
				#culm=csv_file.readline()
				#lin=csv_file.readlines()
				#li=csv_file.read().splitlines()

				li=csv.reader(csv_file)
				he=next(li)
				for lll in li:
					ddd=lll[1:]
					st_li.append(ddd)
					#st_li.append(he1._make(lll))
		df=DataFrame(st_li,columns=columns)

		return df
	def get_txt_line(self,files1):
		st_li=[]
		if os.path.exists(files1):
			with open(files1,'r',encoding='utf-8') as csv_file:
				culm=csv_file.readline()
			print(culm)
			csv_file.close()
		else:
			print('no files1')
		return 0

	def get_excle(self,files1):
		return 0


