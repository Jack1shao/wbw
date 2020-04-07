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
#取4个类型的df
df=kk.get_k_from_csv('600598','D')
cci=hh.cci(df)
print(df)
dw_li2=hh.gj_d_bl(df)
print(dw_li2)
#df=df[-10:]
#tt=rr.two_little('300106','D')


