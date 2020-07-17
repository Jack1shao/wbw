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
import os
#df=ts.get_k_data('603336',ktype='m')
kk=gu_save('')
hh=gu_zb(0)
rr=gu_shou('')
ddd=gu_draw('')

'''#1、临时存入数据
ktype=['30','D','w','m']
tt=['600359','600609','002498',
		'002238','300415','000987',
		'600598','000931','002465']#tt=['all']
for x in ktype:
	kk.pl_chunru(tt,x)'''

#2占位符的作用
str1='kk ll mm oo pp'
~,b,c=str1.split()
*d,l=os.path.split('/houm/offic/kk/ll.csv')
print(a,b,c,d,l)
df=ts.get_hist_data('002498',start='2017-01-01', end='2020-07-18',ktype='30')
print(len(df))
print(df.head())

#ddd.draw_cci3('300316','D')
#print(df.loc[619].date)
print(df[-1:])
#kk.sz_50_2000()


