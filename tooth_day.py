

#获取球探当日的比赛信息
import time,datetime
#获取上个周六，周日
#如果今日非周六，周日
class tooth_dayClass(object):
	"""docstring for tooth_dayClass"""
	def __init__(self, arg):
		super(tooth_dayClass, self).__init__()
		self.arg = arg

	def last_sunday_saturday(self):
		#获取上个周六，周日
		#如果今日非周六，周日
		list_day=[]

		date=datetime.datetime.now()
		yestoday=date+datetime.timedelta(days=-1)
		str_yestoday=yestoday.strftime('%Y-%m-%d')
		list_day.append(str_yestoday)
		day = date.weekday()
		if day<5:
			saturday=date+datetime.timedelta(days=-day-2)
			sunday=date+datetime.timedelta(days=-day-1)
			str_sunday=sunday.strftime('%Y-%m-%d')
			str_saturday=saturday.strftime('%Y-%m-%d')
			list_day.append(str_sunday)
			list_day.append(str_saturday)
		return list_day

#str_today,str_sunday,str_saturday=tooth_dayClass(1).last_sunday_saturday()
#url="https://live.500.com/wanchang.php"

#url2='?e={}'.format(str_sunday)
#print(url+url2)


#print(list3)
#for x in iter(li):	print(x)