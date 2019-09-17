
import itertools
#获取球探当日的比赛信息
import time,datetime
from pandas.core.frame import DataFrame
from functools import reduce
import pandas as pd
import pymysql

#获取上个周六，周日
#如果今日非周六，周日
def last_sunday_saturday():
	#获取上个周六，周日
	#如果今日非周六，周日
	date=datetime.datetime.now()
	day = date.weekday()

	if day<5:
		saturday=date+datetime.timedelta(days=-day-2)
		sunday=date+datetime.timedelta(days=-day-1)
		str_sunday=sunday.strftime('%Y-%m-%d')
		str_saturday=saturday.strftime('%Y-%m-%d')
	return str_sunday,str_saturday

def li_kz(li1,li2):

	li_ret=[]
	for i1 in li1:
		li=[]
		li.append(i1)
		l=set(li)
		if l not in li_ret:
			li_ret.append(l)
		#for i2 in li2:
			
 
	print(li_ret)		
	return li_ret

def li_kz2(li1,li2):
	li_ret=[]
	code=','
	#z=[str(i1)+code+str(i2) for i1 in li1 for i2 in li2  ]
	#for i in itertools.product(li1,repeat=6):
		#print(DataFrame(i))
	fn = lambda x, y: reduce(lambda x, y: [str(i)+code+str(j) for i in x for j in y], x)
	#print(fn(x,code))		
	fn=lambda x, y: [str(i)+code+str(j) for i in x for j in y if str(i)!=str(j)]
	#z=reduce(lambda x, y: x+y, [1,2,3,4,5])
	#z=reduce(fn(li1,li2),[1,2,3,4,5])
	z=fn(li1,li2)
	z=fn(z,li1)
	print(z)
	return 0

def list_in(*li):
	iii=0
	for i in li:
		iii+=1
		print(iii,i)
	return 0


conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='mysql',port=3306,charset='utf8')
#charset用于修正中文输出为问号的问题
sql = "select * from bifa where idnm=784159"
df = pd.read_sql(sql, conn)
print(df.columns.values.tolist())
conn.close

li1=[1,2,3,4,5,6]
li2=[101,102,103,104,105,106]
#z=li_kz2(li1,li1)
#li_kz2(z,li1)
#print(last_sunday_saturday())
#print(last_sunday_saturday())


#print()
#print(list3)
#for x in iter(li):	print(x)