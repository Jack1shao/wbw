import tushare as ts
import datetime
#from getstockClass import getstock
from sqlalchemy import create_engine
import math
from gu_zb import gu_zb
from gu_save import gu_save
from gu_draw import gu_draw
from gu_shou import gu_shou
#df=ts.get_k_data('603336',ktype='m')
kk=gu_save('')
hh=gu_zb(0)
rr=gu_shou('')
ddd=gu_draw('')
#kk.pl_chunru(['600359'],'D')
#print(rr.shou_bc_last_s2('600359'))
#code_list=kk.get_from_csv('shou_d1.txt').code.values.tolist()
#print(code_list)

rr.shou_bc9_all([])
#取4个类型的df
#kk.pl_chunru(['300040'],'D')
#df=kk.get_k_from_api('002301','D')
#MINUS_DI,PLUS_DI,ADX,ADXR=hh.dmi(df)


#print(ADX)
#print(MINUS_DI[-3:])
#print(ADX[-3:])
#ddd.draw_cci3('300316','D')
#print(df.loc[619].date)
#print(df.loc[631].date)
#kk.sz_50_2000()



