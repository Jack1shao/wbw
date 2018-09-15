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
	url='http://odds.500.com/fenxi1/ouzhi.php?id=665021&ctype=1&start=0&r=1&style=0&guojia=0&chupan=1'

	#url='http://odds.500.com/fenxi/ouzhi-664999.shtml'
	header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'}
	request = urllib.request.Request(url, headers=header)
	reponse = urllib.request.urlopen(request)
	decompressed_data = zlib.decompress(reponse.read() ,16+zlib.MAX_WBITS)#压缩包解压，#print(reponse.info())查看
	#一定要关闭，不然会变为攻击
	time.sleep(2)
	reponse.close()
	
	codeing=detect(decompressed_data)#检测编码，	#print(codeing['encoding'])

	if codeing['encoding']=='GB2312':
		codes='gbk' #GB2312 转gbk
	else:
		codes=codeing['encoding']
	#转换编码
	htmlfile = decompressed_data.decode(codes)
	
	return htmlfile

#解析网页文本
def ansy_500wouzhi0(url0):
	bcyclist=['Unibet','IBCBET','12BET','SportingBet']
	ouzhilist=[]
	soup=BeautifulSoup(geturltext(url0),'lxml')
	souplist=soup.find_all(id='table_cont')
	#print(souplist)
	#souplist=soup.find_all('td')
	for tab in souplist:
		#print(1,tab)
		for sps in tab.find_all('span','guojia'):
				sps.decompose()#删除该哦哦你公司国家信息
		list3=[]
		list2=[]
		list1=re.findall('.*?([\u4E00-\u9FA5a-zA-Z0-9.%()]+)',tab.text.strip())
		y=0
		bz=25
		while y+25<len(list1):
			for x in range(bz):
				list2.append(list1[y+x])
				if list1[y+x] in bcyclist:
					y=y+1
			list3.append(list2)
			list2=[]
			y=y+bz
		print(list3)
			# for x in range(10):
			# 	list2.append(itm[x])
			# 	print(list2)
		# for tr1 in tab.find_all('tr'):
		# 	#获取序号
		# 	tagxh=tr1.find('td','td_one')
		# 	#xh=re.findall('\d+',tagxh.text)
		# 	print(tagxh)
		# 	#ouzhilist.append(xh[0])
		# 	#tagxh.decompose()
		# 	#获取菠菜公司
		# 	tagbc=tr1.find('td','tb_plgs')
			#bc=re.findall('',tagbc.text)
			#print(tagbc.text.strip())
			#tagbc.decompose()

			#for td1 in tab.find_all('td'):
			#print(len(td1),td1.text)

			#tdx=td1.find_all('td')
			# td1.decompose()
			#print(td1)
			# if len(tdx)==0:
			# 	ouzhilist.append(td1.text.strip())
			# 	print(td1.text.strip(),0)
			# else:
			# 	for x in tdx:
			# 		print(x.text)
			# 		ouzhilist.append(x.text.strip())
			# td1.decompose()
			#break
			
			
	
	#print(ouzhilist)
		
		
	return ouzhilist

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
	#url='http://odds.500.com/fenxi/ouzhi-664999.shtml'
	#url='http://odds.500.com/fenxi1/ouzhi.php?id=665021&ctype=1&start=1&r=1&style=0&guojia=0&chupan=1'
	driver = webdriver.PhantomJS()
	driver.get(url)
	driver.implicitly_wait(1) 
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