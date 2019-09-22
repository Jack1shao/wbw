
import itertools
#获取球探当日的比赛信息
import time,datetime
from pandas.core.frame import DataFrame
from functools import reduce
import pandas as pd
import pymysql
from loggerClass import logger
import urllib.request
import random
import zlib
from chardet import detect
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver

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

def read_sql():
	pass
	conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='mysql',port=3306,charset='utf8')
	#charset用于修正中文输出为问号的问题
	sql = "select * from yapan where idnm=784159"
	df = pd.read_sql(sql, conn)
	print(df.columns.values.tolist())
	conn.close
	return 0
def t():
	count=7
	url="https://odds.500.com/fenxi/ouzhi-809548.shtml"
	driver = webdriver.Firefox()
	try:
		if (driver.get(url))==None:
			driver.close()
			return ''
		js="var q=document.documentElement.scrollTop=100000"

	except Exception as e:
		print(e)
		driver.close()
	finally:
		#driver.close()

		print(driver)
		
	return  0#htmlfile
def t2():
	# 
	url="https://odds.500.com/fenxi/ouzhi-830867.shtml"
	header = {'Accept': "application/json, text/javascript, */*; q=0.01",
				'Accept-Language': 'en-US,en;q=0.8',
				'Cache-Control': 'max-age=0',
				'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
				'Connection': 'keep-alive',
				'Accept-Encoding':'gzip,deflate',
				'Referer': 'http://www.baidu.com/'
				}
	agentsList =[
					"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
					"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36",
					"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
					"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0"
				]
	#产生随机的User-agent
	ag=random.choice(agentsList)
	req = urllib.request.Request(url, headers=header)
	req.add_header('User-Agent',ag)
	try:
		reponse = urllib.request.urlopen(req)

	#print('get reponse')
	except urllib.error.URLError as e:
			print(e.reason)
			reponse.close()
	zobj = zlib.decompressobj(zlib.MAX_WBITS|16)
	decompressed_data = zobj.decompress(reponse.read())#压缩包解压，#print(reponse.info())查看
	#一定要关闭，不然会变为攻击

	reponse.close()
	#time.sleep(2+random.randint(0,6))
	codeing=detect(decompressed_data)#检测编码，	#print(codeing['encoding'])

	if codeing['encoding']=='GB2312':
		codes='gbk' #GB2312 转gbk
	else:
		codes=codeing['encoding']
	#转换编码
	#print('编码是',codes)
	htmlfile = decompressed_data.decode(codes)
	print(htmlfile)
	return htmlfile

			
#t2()
li1=[1,2,3,4,5,6]
li2=[101,102,103,104,105,106]
list_bifa=['0','0','0','0']
[print(x) for x in list_bifa]

#z=li_kz2(li1,li1)
#li_kz2(z,li1)
#print(last_sunday_saturday())
#print(last_sunday_saturday())


#print()
#print(list3)
#for x in iter(li):	print(x)