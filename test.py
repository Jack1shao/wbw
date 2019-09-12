

#获取球探当日的比赛信息
import time,datetime
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
print(last_sunday_saturday())
print(last_sunday_saturday())


#print()
#print(list3)
#for x in iter(li):	print(x)