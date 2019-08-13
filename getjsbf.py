from gethtmlClass import getHtml
from htmlsoupClass import htmlsoup
from sjfenxi import sjfenxClass
from bs4 import BeautifulSoup
from loggerClass import logger
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
		if x[9] in ['半球'] and x[2]=='0':list3.append(x)
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
def dmdzb(name1,name2):
	'''listdzb=[
							['智利甲', '尤尼昂', '库里科', '08:00', '智利甲', '拉卡莱拉联合', '库里科联队', '08:00', '777040'],
							['墨西联春', '圣路易斯竞技', '蒙特瑞', '06:00', '墨超', '圣路易斯竞技', '蒙特雷', '06:00', '823437'],
							['巴西甲', '阿拉戈亚诺体育队', '格雷米奥', '07:00', '巴西甲', 'CSA阿拉戈诺', '格雷米奥', '07:00', '800399'],
							['巴西乙', '科里蒂巴', '保地花高SP', '07:00', '巴西乙', '科里蒂巴', '博塔弗戈SP', '07:00', '801187'],
							['瑞典超', '赫尔辛堡', '奥雷布洛', '01:00', '瑞典超', '赫尔辛堡', '厄勒布鲁', '01:00', '789270'],
							['韩K联', '蔚山现代', 'FC首尔', '18:30', 'K1联赛', '蔚山现代', 'FC首尔', '18:30', '784087'],
							['欧罗巴杯', '林肯红魔', '阿拉特阿美尼亚', '23:45', '欧罗巴联赛', '林肯红魔', '亚拉腊亚美尼亚', '23:45', '847423'],
							['墨西哥杯', '提华纳', '克雷塔罗', '10:00', '墨西哥杯', '蒂华纳', '克雷塔罗', '10:00', '849068'],
							['欧冠杯', '特拉维夫马卡比', '克卢日', '01:00', '欧冠联赛', '特拉维夫马卡比', '克卢日', '01:00'],
							['巴西乙', '庞特普雷塔', '米内罗美洲', '07:30', '巴西乙', '庞特普雷塔', '米涅罗美洲', '07:30'],
							['日职乙', '横滨FC', '山口雷法', '18:30', 'J2联赛', '横滨FC', '山口雷诺法', '18:30'],
							['欧罗巴杯', '古拉瑞奇', '莫尔德', '02:45', '欧罗巴联赛', '库卡瑞奇', '莫尔德', '02:45'],
							['自由杯', '波特诺山丘', '圣洛伦索', '06:15', '解放者杯', '波特诺山丘', '圣洛伦索', '06:15'],
							['欧罗巴杯', '漫游者(中)', '比尔舒华夏普尔', '22:30', '欧罗巴联赛', '蒙得维的亚流浪者', '贝尔谢巴夏普尔', '22:30'],
							['南球杯', '里加FC', '奥斯杰克', '00:30', '南俱杯', '里加', '奥西耶克', '00:30'],
							['德乙', '桑德豪森', '奥斯纳布鲁克', '00:30', '德乙', '桑德豪森', '奥斯纳布吕克', '00:30'],
							['法乙', '奥兰斯', '查布莱', '02:00', '法乙', '奥尔良', '尚布利', '02:00'],
							['荷甲', '泽沃勒', '威廉二世', '02:00', '荷甲', '兹沃勒', '威廉二世', '02:00'],
							['欧冠杯', '塞萨洛尼基', '阿贾克斯', '01:00', '欧冠联赛', 'PAOK塞萨洛尼基', '阿贾克斯', '01:00'],
							['欧冠杯', '希腊人竞技', '卡拉巴克', '01:00', '欧冠联赛', '希腊人竞技', '卡拉巴赫', '01:00'],
							['巴西乙', '米内罗美洲', '隆迪那', '08:30', '巴西乙', '米涅罗美洲', '隆德里纳', '08:30'],
							['欧罗巴杯', '华沙莱吉亚', '博雷斯拉夫', '03:00', '欧罗巴联赛', '华沙军团', '博莱斯拉夫', '03:00'],
							['欧罗巴杯', '诺科平', '比尔舒华夏普尔', '02:00', '欧罗巴联赛', '北雪平', '贝尔谢巴夏普尔', '02:00'],
							['欧罗巴杯', '布加勒斯特星(中)', '博雷斯拉夫', '02:30', '欧罗巴联赛', '布加勒斯特星队', '博莱斯拉夫', '02:30']
			
						]'''
	listdzb=[
			['兰德斯', '丹麦超', '阿贾克斯青年队', '赫尔蒙德', '兰讷斯', '丹超', '阿贾克斯B队', '赫尔蒙特'] ,
			['丹超', 'U康塞普森', '布加勒斯特星(中)', '诺科平', '丹麦超', '康塞普西翁大学', '布加勒斯特星队', '北雪平'] ,
			['博雷斯拉夫', '华沙莱吉亚', '隆迪那', '卡拉巴克', '博莱斯拉夫', '华沙军团', '隆德里纳', '卡拉巴赫'] ,
			['塞萨洛尼基', '泽沃勒', '查布莱', '奥兰斯', 'PAOK塞萨洛尼基', '兹沃勒', '尚布利', '奥尔良'] ,
			['奥斯纳布鲁克', '奥斯杰克', '里加FC', '南球杯', '奥斯纳布吕克', '奥西耶克', '里加', '南俱杯'] ,
			['比尔舒华夏普尔', '漫游者(中)', '自由杯', '古拉瑞奇', '贝尔谢巴夏普尔', '蒙得维的亚流浪者', '解放者杯', '库卡瑞奇'] ,
			['山口雷法', '日职乙', '米内罗美洲', '欧冠杯', '山口雷诺法', 'J2联赛', '米涅罗美洲', '欧冠联赛'] ,
			['提华纳', '阿拉特阿美尼亚', '欧罗巴杯', '韩K联', '蒂华纳', '亚拉腊亚美尼亚', '欧罗巴联赛', 'K1联赛'] ,
			['奥雷布洛', '保地花高SP', '阿拉戈亚诺体育队', '蒙特瑞', '厄勒布鲁', '博塔弗戈SP', 'CSA阿拉戈诺', '蒙特雷'] ,
			['墨西联春', '库里科', '尤尼昂', 'J联赛', '墨超', '库里科联队', '拉卡莱拉联合', '日职联'] 

			]
	#整理
	listzl=[]
	for li in listdzb:
		for x in range(0,4):
			
			if li[x]==li[x+4]:continue
			list11=[]
			list11.append(li[x])
			list11.append(li[x+4])

			if (list11 not in listzl):

				listzl.append(list11)
	#print(listzl)
	
	listdzb3=[]
	while len(listzl)>0:
		#print(len(listzl))
		listdzb2=[]
		for x in range(0,4):
			if len(listzl)==0:break
			i=listzl.pop();
			listdzb2.insert(x,i[0])
			listdzb2.insert(x+4,i[1])
		if len(listdzb2)!=8:
			l=int(len(listdzb2)/2)
			i=(4-l)
			
			for x in range(0,int(i)):
					listdzb2.insert(l+x,'0')
					listdzb2.insert(l+x+4,'0')
		if len(listdzb2)==8 :
			listdzb3.append(listdzb2)
			
	#for 的写法
	#[print(li,',') for li in listdzb3 if 1==1]


	#名字相等
	if name1==name2:return 1
	#名字在对照表中
	#print(name1,name2,levle)
	for x in listdzb3:
		for xx in range(0,4):
			if  x[xx]==name1 and x[xx+4]==name2:return 1
			if  x[xx]==name2 and x[xx+4]==name1:return 1
		
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
				bz=bz*dmdzb(qt[x],wbw[x])
			if bz:
				listls.append(wbw)
				break

			#辅助对照

			if bz==0 and qt[3]==wbw[3] and dmdzb(qt[0],wbw[0]) and (dmdzb(qt[1],wbw[1]) or dmdzb(qt[2],wbw[2])):

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
	print("jieshui")
	
	return listls


def getdcsj(id1):
	print(str(id1)+"获取比赛数据。。。")
	hs=htmlsoup(id1)
	#scblist,bzsc=hs.getsc()
	ozlist,bzoz=hs.getouzhi()
	#yplist,bzyp=hs.getyapan()
	#bflist,bzbf,bflist_sjtd=hs.getbifa()

	#if bzsc*bzoz*bzyp*bzbf==0:print("date error...");return 0

	#return 1,scblist,ozlist,yplist,bflist,bflist_sjtd
	return ozlist




#获取半球的id号
def get_id_list(datlist):
	idlist=[]
	for li in datlist:
		idlist.append(li[4])
	return idlist
	

#写入文件
def wr_into_log(datlist):
	lg=logger()
	lg.info(datlist)
	for x in datlist:
		id1=int(x)
		j=sjfenxClass(id1)
		j.bd()
	
#测试。。。。。。。。。	
#dmdzb('','')
#获取半球盘的比赛id
li=(get_id_list(hb()))
wr_into_log(li)
