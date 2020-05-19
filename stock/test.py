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
#df=kk.get_k_from_csv('002498','D')
print (rr.shou_bc_last_s('002498'))
#cci=hh.cci(df)
#print(cci)
#print(rr.shou_cci_D_qrs('603019'))
#ddd.draw_cci3('300316','D')
#print(df.loc[538])
#print(df.loc[555])
#rr.buy_3(df)
#kk.sz_50_2000()
#print(code_li)


