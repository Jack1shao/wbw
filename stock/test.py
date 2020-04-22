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
#取4个类型的df
#list11=['002498']
#kk.pl_chunru(list11,'30')
df=kk.get_k_from_csv('002498','30')
up,dw=hh.gj_bl(df)
print(up)
#ddd.draw_cci3('300316','D')
#print(df.loc[454])
#print(df.loc[475])
#rr.buy_3(df)
#kk.sz_50_2000()
#print(code_li)


