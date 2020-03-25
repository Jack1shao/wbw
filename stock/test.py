import tushare as ts
import datetime
#from getstockClass import getstock
from sqlalchemy import create_engine

#df=ts.get_k_data('603336',ktype='m')
df = ts.get_stock_basics()
print(df)