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
df=kk.get_k_from_csv('600999','D')
print(hh.ma(df))
#df=ts.get_concept_classified()
print (df)
#cci=hh.cci(df)
#print(cci)
#print(rr.shou_cci_D_qrs('603019'))
#ddd.draw_cci3('300316','D')
#print(df.loc[454])
#print(df.loc[475])
#rr.buy_3(df)
#kk.sz_50_2000()
#print(code_li)


