from gethtmlClass import getHtml
from bs4 import BeautifulSoup
import re
def gethtmlsoup(url):
	#500w北单比方情况
	url="https://live.500.com/zqdc.php"
	
	#url="https://live.500.com/2h1.php"
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
	#print(list31[1])
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
		#比分
		listbcbf=tdlist[8].get_text().split('-')
		#print(listbcbf)
		#list连接成一个
		listgy.extend(listsj)
		listgy.extend(idlist)
		if listbcbf[0]==' ':
			bsxxlist.append(listgy)
			
	
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
		if x[9] in ['半球','受半球'] and x[2]=='0':list3.append(x)
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
#球队名称对照
def dmdzb(name1,name2,levle):
	listdzb=[
				['智利甲', '尤尼昂', '库里科', '08:00', '智利甲', '拉卡莱拉联合', '库里科联队', '08:00', '777040'],
				['墨西联春', '圣路易斯竞技', '蒙特瑞', '06:00', '墨超', '圣路易斯竞技', '蒙特雷', '06:00', '823437'],
				['巴西甲', '阿拉戈亚诺体育队', '格雷米奥', '07:00', '巴西甲', 'CSA阿拉戈诺', '格雷米奥', '07:00', '800399'],
				['巴西乙', '科里蒂巴', '保地花高SP', '07:00', '巴西乙', '科里蒂巴', '博塔弗戈SP', '07:00', '801187'],
				['瑞典超', '赫尔辛堡', '奥雷布洛', '01:00', '瑞典超', '赫尔辛堡', '厄勒布鲁', '01:00', '789270'],
				['韩K联', '蔚山现代', 'FC首尔', '18:30', 'K1联赛', '蔚山现代', 'FC首尔', '18:30', '784087'],
				['欧罗巴杯', '林肯红魔', '阿拉特阿美尼亚', '23:45', '欧罗巴联赛', '林肯红魔', '亚拉腊亚美尼亚', '23:45', '847423'],
				['墨西哥杯', '提华纳', '克雷塔罗', '10:00', '墨西哥杯', '蒂华纳', '克雷塔罗', '10:00', '849068'],
				['欧冠杯', '特拉维夫马卡比', '克卢日', '01:00', '欧冠联赛', '特拉维夫马卡比', '克卢日', '01:00'],
				['巴西乙', '庞特普雷塔', '米内罗美洲', '07:30', '巴西乙', '庞特普雷塔', '米涅罗美洲', '07:30']
			]
	
	#名字相等
	if name1==name2:return 1
	#名字在对照表中
	#print(name1,name2,levle)
	for x in listdzb:
		for xx in range(0,4):
			if  x[xx]==name1 and x[xx+4]==name2:return 1
		
	return 0


def hb():
	print("开始获取....")
	listwbw=get500wzqdc(gethtmlsoup(''))

	#整理500万数据
	listwbw1=[]
	for wbw in listwbw:
		del wbw[3]
		listwbw1.append(wbw[0:5])
	#print(listwbw1)
	listqt=getqtzqdc()
	print("球探数据")
	print(listqt)
	#
	listls=[]
	for qt in listqt:
		for wbw in listwbw1:
			#if qt[3]!=wbw[3]:break#比赛时间相等
			bz=1
			#队名和比赛时间相等
			for x in range(0,4):
				bz=bz*dmdzb(qt[x],wbw[x],x)
			if bz:
				listls.append(wbw)
				break

			#辅助对照

			if bz==0 and qt[3]==wbw[3] and (qt[0]==wbw[0] or qt[1]==wbw[1] or qt[2]==wbw[2]):
				print("辅助对照：")
				l1=[]
				l2=[]
				for x in range(0,4):
					l2.append(wbw[x])
					l1.append(qt[x])
				l1.extend(l2)
				print(l1)
				l1.clear()

	print("比对结果：")		
	print(listls)

	#listjj=set(listwbw1).intersection(set(listqt))
	#print(listjj)
	#整理球探数据

	
#url="https://live.500.com/zqdc.php"
#get500wzqdc(gethtmlsoup(' '))
hb()
#print(dmdzb('墨西联春','墨超',0))
#getqtzqdc()