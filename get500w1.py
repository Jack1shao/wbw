import urllib.request
from bs4 import BeautifulSoup
import zlib
import re
from selenium import webdriver
from chardet import detect
import time

#获取网页文本
#
def geturltext(url):

	header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'}
	request = urllib.request.Request(url, headers=header)
	reponse = urllib.request.urlopen(request)
	decompressed_data = zlib.decompress(reponse.read() ,16+zlib.MAX_WBITS)#压缩包解压，#print(reponse.info())查看
	#一定要关闭，不然会变为攻击
	time.sleep(4)
	reponse.close()
	
	codeing=detect(decompressed_data)#检测编码，	#print(codeing['encoding'])

	if codeing['encoding']=='GB2312':
		codes='gbk' #GB2312 转gbk
	else:
		codes=codeing['encoding']
	#转换编码
	htmlfile = decompressed_data.decode(codes)
	
	return htmlfile

def gettextsoup(textfile):
	return
def getyapan(id1):

	pass


def getbsxx(soup):
	bsxxlist=[]
	soupdz=soup.find_all('a','hd_name')

	if len(soupdz)==3:
		bsxxlist.append(soupdz[0].text.strip())
		bsxxlist.append(soupdz[2].text.strip())

		str11=soupdz[1].text.strip()
		bsxxlist.append(str11[0:5])#取年份
		ls=re.findall('.*?([\u4E00-\u9FA5]+)',str11)
		bsxxlist.append(ls[0][0:-1])#去掉‘第’字。联赛
		lun=re.findall('\d+',str11[6:])
		bsxxlist.append(lun[0])#获取轮次
		
	else:print('错误10001')
	

	#获取比分
	soupbf=soup.find('p','odds_hd_bf')
	jqs=re.findall('\d+',soupbf.text)
	[bsxxlist.append(x) for x in jqs]
		
	#获取比赛时间
	souptime=soup.find('p','game_time')
	bsxxlist.append(souptime.text.strip('比赛时间'))
	
	
	print(bsxxlist)

	return bsxxlist

#解析网页文本,获取500W欧指的前30个博彩哦你公司
#由于该网站是通过滚轴；按30个数据加载的，所以要
def ansy_500wouzhi01(id1):
	#url0='http:???fenxi1/ouzhi.php?id=665021&ctype=1&start=30&r=1&style=0&guojia=0&chupan=1'
	id1=665021
	url0='http://odds.500.com/fenxi1/ouzhi.php?id='+str(id1)+'&ctype=1&start=0&r=1&style=0&guojia=0&chupan=1'
	ouzhilist=[]
	soup=BeautifulSoup(geturltext(url0),'lxml')
	getbsxx(soup)



	souphtml=soup.find_all(id='nowcnum')
	#获取欧赔公司数量
	cnum=re.findall('\d+',souphtml[0].text)
	a=int(int(cnum[0])/30)#除30向下取整数

	for x in range(a):
		ouzhilist=ouzhilist+ansy_500wouzhi02(id1,30*(x+1))
	

	souplist=soup.find_all(id='table_cont')
	list3=[]
	for tab in souplist:
		
		for sps in tab.find_all('span','guojia'):
				sps.decompose()#删除该哦哦你公司国家信息
				
		list1=re.findall('.*?([\u4E00-\u9FA5a-zA-Z0-9.%()]+)',tab.text.strip())
		
		y=0
		bz=25

		while y+25<len(list1):
			list2=[]
			for x in range(bz):
				list2.append(list1[y+x])
				if x==24 and x+y+25<=len(list1) and list1[y+x]=='同' and list1[y+x+25]=='客':
					#删除博彩公司后面的异常数据，
					list1.pop(x+y+3)

			list3.append(list2)
			
			y=y+bz
		
			
	ouzhilist=list3+ouzhilist
	print(ouzhilist)
	return ouzhilist

def ansy_500wouzhi02(id1,starts):
	url0='http://odds.500.com/fenxi1/ouzhi.php?id='+str(id1)+'&ctype=1&start='+str(starts)+'&r=1&style=0&guojia=0&chupan=1'
	ouzhilist=[]
	list3=[]
	soup=BeautifulSoup(geturltext(url0),'lxml')
	# print(soup)
	for tab in soup:
		
		for sps in tab.find_all('span','guojia'):
				sps.decompose()#删除该哦哦你公司国家信息
				
		list1=re.findall('.*?([\u4E00-\u9FA5a-zA-Z0-9.%()-]+)',tab.text.strip())
		
		y=0
		bz=25
		while y+25<len(list1):
			list2=[]
			for x in range(bz):
				list2.append(list1[y+x])
				if x==24 and x+y+25<=len(list1) and list1[y+x]=='同' and list1[y+x+25]=='客':
					#删除博彩公司后面的异常数据，
					list1.pop(x+y+3)

			list3.append(list2)
			
			y=y+bz
		#print(list3)

	return list3

def getyapan01(id):
	id=665021
	url0='http://odds.500.com/fenxi/yazhi-665021.shtml?ctype=2'
	ouzhilist=[]
	soup=BeautifulSoup(geturltext(url0),'lxml')
	souplist=soup.find_all(id='table_cont')
	yclist=['主', '客', '同','升', '(优胜客)','(明升)','降','(壹貳博)']
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
		
		if lenlist2%8==0:

			while y+bz<=lenlist2 and y/bz<10:
				list4=[]
				for x in range(bz):
					list4.append(list2[x+y])
				y=y+bz
				list3.append(list4)



		else:
			print('错误00002')
			return 0
		
		

	print(list3)
	
	return list3






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
	#url='http://o/fenxi/ouzhi-664999.shtml'
	#url='http://odd/fenxi1/ouzhi.php?id=665021&ctype=1&start=1&r=1&style=0&guojia=0&chupan=1'
	driver = webdriver.PhantomJS()
	driver.get(url)
	driver.implicitly_wait(3) 
	souphtml=driver.find_element_by_id('table_cont').text
	print(souphtml)
	# data = driver.title
	data=driver.page_source
	#print(detect(data))
	driver.close()
	#print(data.encode("gb2312","ignore").decode("gb2312"))
	return


#geturltext('')
# souphtml('')
#selum('')
ansy_500wouzhi0('')