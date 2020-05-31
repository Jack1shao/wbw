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
#kk.pl_chunru(['300040'],'D')
df=kk.get_k_from_api('002301','D')
MINUS_DI,PLUS_DI,ADX,ADXR=hh.dmi(df)

#print(ADX)
#print(MINUS_DI[-3:])
print(ADX[-3:])
#print(hh.cci_qsqy(df))
#print (rr.shou_bc_last_s('300040'))
#cci=hh.cci(df)
#print(cci)
#print(rr.shou_cci_D_qrs('603019'))
#ddd.draw_cci3('300316','D')
#print(df.loc[619].date)
#print(df.loc[631].date)
#rr.buy_3(df)
#kk.sz_50_2000()
#print(code_li)


