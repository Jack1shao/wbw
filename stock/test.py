import tushare as ts
import datetime
df=ts.get_today_all()
#df=ts.get_hist_data('600848')
#df=ts.get_h_data('600848',start='2000-01-05',end='2019-01-09')
#print(df['date'])
#print(df.columns)
#Index(['code', 'name', 'changepercent', 'trade', 'open', 'high', 'low','settlement', 'volume', 'turnoverratio', 'amount', 'per', 'pb',
#       'mktcap', 'nmc'],

'''for i in range(10-1,-1,-1):
	print(i)
for i in range(0,10,1):
	print(i)'''
now = datetime.datetime.now().strftime('%Y-%m-%d')
now2 = datetime.datetime.now().strftime('%H:%M')
df['now']=now
df['now2']=now2
print(df.head())
print(now,now2)

#存入数据库
df.to_sql('tick_data',engine)

#追加数据到现有表
#df.to_sql('tick_data',engine,if_exists='append')