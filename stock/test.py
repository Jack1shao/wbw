import tushare as ts
import datetime

from sqlalchemy import create_engine
import math
from gu_zb import gu_zb
from gu_save import gu_save
from gu_draw import gu_draw
from gu_shou import gu_shou
from stockmd import stockzb
from stockmd import m_kl
from stockmd import w_kl
from stockmd import D_kl
from stockmd import Hf_kl
from stockmd import jiekou
#from stockmd2 import cciorder
import os


kk=gu_save('')

hh=gu_zb(0)
rr=gu_shou('')
ddd=gu_draw('')
jk=jiekou()

#pro = ts.pro_api('4d4e8c66f3fe804a585a345419362a9982790682a79ef65214b5d5e1')
#pro = ts.pro_api()
#df = pro.daily(ts_code='000001', start_date='20150701', end_date='20160718')
#print(df.columns.values.tolist())
#
df=ts.get_k_data('603336',ktype='D')
print(df.columns.values)
class queue:
	def __init__(self,maxsize=0):
		self.maxsize=maxsize
		self.__list=[]
	def put(self,item):
		if len(self.__list)>=self.maxsize:
			self.__list.pop(0)
		self.__list.append(item)
		return 0

	def get(self):
		return self.__list
q=queue(maxsize=3)


#1、临时存入数据
ktype=['30','D','w','m']

print(ktype[3])
tt=['002371','600609','002498',
		'002238','300415','000987',
		'600598','000931','002465']#tt=['all']
for x in ktype:
	#kk.pl_chunru(tt,x)
	
	q.put(x)
	print(q.get())



#2占位符的作用
str1='kk ll mm oo pp'
*a,b,c=str1.split()
*d,l=os.path.split('/houm/offic/kk/ll.csv')
print(a,b,c,d,l)
#print(df.loc[619].date)

i=3
b=5

y=b-2 if b-2>=0 else 0
for x in range(b-1,y-1,-1):
	print(x)
