import urllib.request
from bs4 import BeautifulSoup
import zlib
import re
from selenium import webdriver
from chardet import detect
import time
import pymysql
import random
from gzip import GzipFile
import io
import datetime

def gzip(data):
	buf = io.BytesIO(data)
	f = gzip.GzipFile(fileobj=buf)
	return f.read()

def deflate(data):
	try:
		return zlib.decompress(data, 16+zlib.MAX_WBITS)
	except zlib.error:
		return zlib.decompress(data)

#获取一个数据库连接
def insertMysql(dateIn,SqlInsert):

	try:
		conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='mysql',port=3306,charset='utf8')
		cur=conn.cursor()#获取一个游标
		
		cur.executemany(SqlInsert,dateIn)
		#print(dateIn)
		print('插入成功');
		conn.commit()
		cur.close()#关闭游标
		conn.close()#释放数据库资源
	except  Exception as e :print("insert 发生异常",e);return 0
	return 1

def selectMysql(sql):
	dateList=[]
	#获取一个数据库连接
	try:
		dateList=[]
		conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='mysql',port=3306,charset='utf8')
		cur=conn.cursor()#获取一个游标
		cur.execute(sql)
		dateList=cur.fetchall()
		conn.commit()
		cur.close()#关闭游标
		conn.close()#释放数据库资源
	except  Exception as e :print("发生异常",e);return 0
	return dateList


def tempselect():
	sql="select idnm from scb"
	print(selectMysql(sql))
	return 0

def bsid_from_db(idstart,idend):
	sql="select idnm from scb where idnm between " +str(idstart)+" and " +str(idend)
	return selectMysql(sql)
	


def getbsxx(id1,soup):
	bsxxlist=[]
	bsxxlist.append(str(id1))
	soupdz=soup.find_all('a','hd_name')

	if len(soupdz)==3:
		bsxxlist.append(soupdz[0].text.strip())
		bsxxlist.append(soupdz[2].text.strip())

		str11=soupdz[1].text.strip()
		bsxxlist.append(str11[0:2])#取年份
		ls=re.findall('.*?([\u4E00-\u9FA5]+)',str11)
		bsxxlist.append(ls[0][0:-1])#去掉‘第’字。联赛
		print(str11[-3:],str11)
		lun=re.findall('\d+',str11[-3:])
		if len(lun)>0:bsxxlist.append(lun[0])#获取轮次
		else:bsxxlist.append('-1')
		
		
	else:print('错误10001')
	

	#获取比分
	soupbf=soup.find('p','odds_hd_bf')
	jqs=re.findall('\d+',soupbf.text)
	[bsxxlist.append(x) for x in jqs]
		
	#获取比赛时间
	souptime=soup.find('p','game_time')
	bsxxlist.append(souptime.text.strip('比赛时间'))
	print(bsxxlist)
	list3=[]
	list3.append(bsxxlist)
	return list3


#取得文本可多次使用 
#return soup
def gethtmlsoup(url0):

	soup=BeautifulSoup(geturltext(url0),'lxml')
	return soup


#解析网页文本,获取500W欧指
# return list
def ansy_500wouzhi(id1,soup):
	list3=[]
	yclist=['主客', '同']
	for tab in soup:
		for sps in tab.find_all('span','guojia'):
				sps.decompose()#删除该哦哦你公司国家信息
				
		list1=re.findall('.*?([\u4E00-\u9FA5a-zA-Z0-9.()-]+)',tab.text.replace(' ',''))
		y=0
		bz=24
		while y+bz<=len(list1):
			list2=[]
			list2.append(str(id1))
			for x in range(bz):
				if list1[y+x] not in yclist:
					list2.append(list1[y+x])
				if x==23 and x+y+bz<=len(list1) and list1[y+x]=='同' and list1[y+x+bz]=='主客':
					#删除博彩公司后面的异常数据，
					list1.pop(x+y+3)
			list3.append(list2)
			y=y+bz
	return list3

#获取欧赔公司数量
#return int
def getbcgscount(soup):
	souphtml=soup.find_all(id='nowcnum')
	
	cnum=re.findall('\d+',souphtml[0].text)
	a=int(cnum[0])-2
	return a


#获取欧指
def getouzhi(id1):
	
	starts=0
	url0='http://odds.500.com/fenxi1/ouzhi.php?id='+str(id1)+'&ctype=1&start='+str(starts)+'&r=1&style=0&guojia=0&chupan=1'
	soup=gethtmlsoup(url0)
	dateinbsxx=getbsxx(id1,soup)
	put_bsxx_in_db(dateinbsxx)#插入比赛信息，scb

	put_ouzhi_in_db(ansy_500wouzhi(id1,soup.find_all(id='table_cont')))
	#
	a=getbcgscount(soup)-1
	for x in range(int(a/30)):
		starts=30*(x+1)
		url0='http://odds.500.com/fenxi1/ouzhi.php?id='+str(id1)+'&ctype=1&start='+str(starts)+'&r=1&style=0&guojia=0&chupan=1'
		soup2=gethtmlsoup(url0)
		put_ouzhi_in_db(ansy_500wouzhi(id1,soup2))

	return 0



#获取网页文本
#
def geturltext(url):

	header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
			'Accept-Encoding':'gzip,deflate'}
	request = urllib.request.Request(url, headers=header)
	try:
		reponse = urllib.request.urlopen(request)
		#print('get reponse')
	except urllib.error.URLError as e:
    		print(e.reason)
    		reponse.close()

	zobj = zlib.decompressobj(zlib.MAX_WBITS|16)
	decompressed_data = zobj.decompress(reponse.read())#压缩包解压，#print(reponse.info())查看
	#一定要关闭，不然会变为攻击
	
	reponse.close()
	time.sleep(2+random.randint(0,3))
	codeing=detect(decompressed_data)#检测编码，	#print(codeing['encoding'])

	if codeing['encoding']=='GB2312':
		codes='gbk' #GB2312 转gbk
	else:
		codes=codeing['encoding']
	#转换编码
	print('编码是',codes)
	htmlfile = decompressed_data.decode(codes)
	
	return htmlfile



#插入数据库-比赛信息
#
def put_bsxx_in_db(dateIn):
	sql="insert into scb values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	insertMysql(dateIn,sql)
	return 1
	

#插入数据库-欧赔
def put_ouzhi_in_db(dateIn):
	sql="insert into ouzhi values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	insertMysql(dateIn,sql)
	return 1

#插入数据库-亚盘
def put_yapei_in_db(dateIn):
	SqlInsert="insert into yapan values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	#dateIn=[['665022', '1', '澳门', '1.980', '受球半', '0.820', '0.920', '受球半/两球', '0.880'], ['665022', '2', 'Bet365', '1.060', '受球半', '0.870', '1.154', '受球半', '0.760']]
	insertMysql(dateIn,SqlInsert)
	return 1



def getyapan(data1):
	soup=BeautifulSoup(data1,'lxml')
	return soup
#由于该网站是通过滚轴；按30个数据加载的，所以要

def getyapan01(id1):
	
	url0='http://odds.500.com/fenxi/yazhi-'+str(id1)+'.shtml?ctype=2'
	ouzhilist=[]
	#data1=selum(url0)
	#soup=getyapan(data1)
	soup=BeautifulSoup(geturltext(url0),'lxml')
	souplist=soup.find_all(id='table_cont')
	yclist=['主', '客', '同','升', '(优胜客)','(明升)','降','(壹貳博)','(沙巴)']
	y=0
	bz=8
	list3=[]
	for tab in souplist:
		
		for sps in tab.find_all('span','guojia'):
			sps.decompose()#删除该哦哦你公司国家信息guojia
		for sps in tab.find_all('span','tb_tdul_more'):
			sps.decompose()#删除该哦哦你公司国家信息tb_tdul_more
		for times in tab.find_all('time'):
			times.decompose()

		list1=re.findall('.*?([\u4E00-\u9FA5a-zA-Z0-9.%()/]+|[0-9]+-[0-9]+)',tab.text.strip())
		
		list2=[]

		for x in range(len(list1)):
			if list1[x] not in yclist:
				list2.append(list1[x])
		lenlist2=len(list2)
		#print(list2)
		if lenlist2%bz==0:

			while y+bz<=lenlist2 and y/bz<10:
				list4=[]
				list4.append(str(id1))
				for x in range(bz):
					list4.append(list2[x+y])
				y=y+bz
				list3.append(list4)
		else:
			print('错误00002')
			return 0
	#print(list3)
	put_yapei_in_db(list3)
	return 0



def souphtml(html1):
	# soup = BeautifulSoup(open('500w.html'))#打开本地文本
	soup = BeautifulSoup(geturltext('500w.html'),'lxml')
	#soup = BeautifulSoup(html1,'lxml')
	# print(soup.title.string)
	# print(soup.find_all(id='table_cont'))
	print(soup.text)
	# for tab in soup.find_all(id='table_cont'):
		
	# 	#print(tab.text)
	# 	print(re.findall('.*?([\u4E00-\u9FA5]+|[a-zA-Z]+|[0-9]+.[0-9%]+|[0-9]+)',tab.text))
	return 0
#用静默浏览器，适用动态加载
def selum(url):
	
	driver = webdriver.PhantomJS()
	driver.get(url)
	driver.implicitly_wait(3) 
	#souphtml=driver.find_element_by_id('table_cont').text
	data=driver.page_source
	driver.close()
	return  data

def getbsid(idstart,idend):
	
	jsq=0#计数器
	list1=[]
	if idstart>idend:return 0
	idlist=bsid_from_db(idstart,idend)
	for idnmrow in idlist:
			for idnm0 in idnmrow:
				list1.append(idnm0)
	#print(list1)
	for x in range(idstart,idend+1):
		if x not in list1:
			jsq=jsq+1
			if jsq>50:#50条停一分钟
				time.sleep(60)
				print('wait a moment-60seconds')
				jsq=0
			print('开始获取',x,jsq)
			#print("开始获取亚盘")
					
			#插入数据库
			getouzhi(x)
			getyapan01(x)
	print(datetime.datetime.now())
	return 0
			


#getouzhi(665021)
#['法甲','1718','664725','665104']
#['德甲','1718','672920','673225']
#['瑞典超','17','633991','634230']
#['瑞典超','18','707696','707863']
#['日职','17','647803','648108']
#['日乙','18','713219','713588']
#['k1联','18','715319','715488']
#['挪超','17','630624','630863']
#['荷甲','17','663521','663826']
#['德乙','17','673226','673531']
#['丹超','17','665106','665287']
#['俄超','17','666163','666402']
#['芬超','18','719170','719343']

getbsid(666163,666402)
#getyapan01(673112)