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
#df=ts.get_k_data('603336',ktype='m')
kk=gu_save('')
hh=gu_zb(0)
rr=gu_shou('')
ddd=gu_draw('')

'''ktype=['30','D','w','m']
tt=['600359','600609','002498',
		'002238','300415','000987',
		'600598','000931','002465']#tt=['all']
for x in ktype:
	kk.pl_chunru(tt,x)'''
#print(rr.shou_bc_last_s2('600359'))
#code_list=kk.get_from_csv('shou_d1.txt').code.values.tolist()
#print(code_list)

#rr.shou_all_d()
#取4个类型的df
#kk.pl_chunru(['300040'],'D')
code='002498'
type1='30'
df=kk.get_k_from_api(code,type1)
df2=df[60:300]
#print(df2)
dat11=df2.iloc[-1:].date.values[0].split()[0]
#print(dat11)
file1='{0}-{1}-bak-{2}.csv'.format(code,type1,dat11)
#df2.to_csv('002498-30-bak-20200527.csv')
print(file1)
#MINUS_DI,PLUS_DI,ADX,ADXR=hh.dmi(df)


#print(ADX)
#print(MINUS_DI[-3:])
#print(ADX[-3:])
#ddd.draw_cci3('300316','D')
#print(df.loc[619].date)
#print(df.loc[631].date)
#kk.sz_50_2000()


