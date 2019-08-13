'''
getyahoo

'''
from sqlalchemy import create_engine
from matplotlib.pylab import date2num
import tushare as ts
import pandas as pd
import pymysql;
import datetime;
import time;
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
from matplotlib.finance import quotes_historical_yahoo_ochl

ticker = '600028.ss'
date1 = datetime.date( 2015, 1, 10 )  
date2 = datetime.date( 2016, 1, 10 )  
  
#daysFmt  = DateFormatter('%m-%d-%Y')  
  
quotes = quotes_historical_yahoo_ochl(ticker, date1, date2)
print(quotes)