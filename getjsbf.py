from gethtmlClass import getHtml
from bs4 import BeautifulSoup
import re
def gethtmlsoup(url):
	#500w北单比方情况
	url="https://live.500.com/zqdc.php"
	htmltext=getHtml().geturltext(url)
	soup=BeautifulSoup(htmltext,'lxml')
	return soup
#500w北单比方情况
#用find和get 获取数据
def get500wzqdc(soup):
	#
	print("获取500w比赛单场数据")
	listtable=soup.find_all(id='table_match')
	list31=listtable[0].find_all('tr')
	bsxxlist=[]
	for x in list31:
		#获取500w比赛id
		id1=x.get('fid')
		if id1==None: continue
		idlist=[]
		idlist.append(id1)	
		#获取联赛的球队
		listgy=(x.get('gy').split(','))
		tdlist=x.find_all('td')
		#获取比赛时间
		listsj=(tdlist[3].get_text().split(' '))
		#list连接成一个
		listgy.extend(listsj)
		listgy.extend(idlist)
		bsxxlist.append(listgy)
	#print(bsxxlist)
	return bsxxlist

#获取球探当日的比赛信息
def getqtzqdc():
	print("获取球探当日比赛单场数据")
	h=getHtml()
	t1=h.getHtml_by_firefox("http://live.win007.com/index2in1.aspx?id=8")
	
	li=re.findall('.*?([\u4E00-\u9FA5a-zA-Z0-9.:/()-]+)',t1)
	list1=[]
	list2=[]
	for x in iter(li):

		list1.append(x)
		
		if x=='欧':list2.append(list1);list1=[]
		if x=='数据':list1=[]   
		if x==')':break;

	list3=[]
	for x in iter(list2):
		#同步开场未开场数据
		if x[3]=="-":x.insert(2,'0')
		#修复半场数据信息
		if not re.findall('-',x[6]):x.insert(6,'-')
		if x[9] in ['半球','受半球'] and x[2]=='0':list3.append(x);#print(x)
	#print(list3)
	
	list5=[]
	for x in list3:
		list4=[]
		list4.append(x[0])
		list4.append(x[3])
		list4.append(x[5])
		list4.append(x[1])
		list5.append(list4)
	
	#print(list5)	
	return list5

def hb():
	listwbw=get500wzqdc(gethtmlsoup(''))

	#整理500万数据
	listwbw1=[]
	for wbw in listwbw:
		del wbw[3]
		listwbw1.append(wbw[0:5])
	print(listwbw1)
	listqt=getqtzqdc()
	print("球探数据")
	print(listqt)
	#
	listls=[]
	for qt in listqt:
		for wbw in listwbw1:
			if qt[3]==wbw[3] and (qt[0]==wbw[0] or qt[1]==wbw[1] or qt[2]==wbw[2]):
				#listddd=qt.extend(wbw)
				print(qt,wbw)

				listls.append(wbw)
			
	print(listls)

	#listjj=set(listwbw1).intersection(set(listqt))
	#print(listjj)
	#整理球探数据

	pass
#url="https://live.500.com/zqdc.php"
#getid(gethtmlsoup(url))
hb()
#getqtzqdc()