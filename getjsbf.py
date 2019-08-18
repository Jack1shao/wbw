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
	htmltext=h.getHtml_by_firefox("http://live.win007.com/index2in1.aspx?id=8")
	soup=BeautifulSoup(htmltext,'lxml')
	#获取主要表格
	ss=soup.find_all('table',id="table_live")

	list2=[]
	for tb in ss[0:2]:
		row=tb.find_all("tr")
		for cell in row:
			cc=cell.find_all('td')
			#去除干扰
			if len(cc)<2:continue
			i=0
			list1=[]
			
			for x in cc:
				i+=1
	
				xstr=x.text
				if xstr=='选' :break
				if xstr=='':xstr='-'
				if cc.index(x)==9: 
					#print(i,cc.index(x),x)
					xstr=x.find_all('div',attrs={'class':'odds1'})[0].text
				list1.append(xstr)
			if len(list1)>1:
				list2.append(list1)
			
	#print(list2[1:3])
	#不需要的联赛
	listbxy=['德地区东北', '中甲', '中女超',  '德丙', '德地区巴', '德地区南', '德地区北',  '越南联', '爱沙甲', '哈萨超', '瑞典丙OG', '泰超', '乌兹超']
	l2=['立陶乙', '泰甲', 	'英女超', '德堡州联', '挪女甲', '德女联', '奥女甲',  '挪乙A', '挪乙B', '挪女超',  '马来杯', '球会友谊', '瑞典女超', '德戊', '巴圣杯' ]
	l3=['奥丙WS', '英U23A', '巴圣塔乙',	'巴圣青联', '苏女超',   '瑞典乙北', '土甲', '格鲁乙', '英议联',  '拉脱超', '斯亚甲', '巴青锦',  '瑞典乙南', '意丙杯','芬乙B', '芬乙A' ]
	l4=['芬乙C', '意杯', '以超图杯', '土超', '以甲图杯',  '墨西乙春',	 '乌拉甲', '厄瓜甲春', '巴女甲', '阿乙', '秘鲁甲秋', '阿乙曼特', '巴丙B', '玻利甲秋', '巴丙A', '智利乙' ]
	l5=['委內超秋', '哥斯甲',  '美乙', '新西南联', '澳塔挑联', 	 '美女职', '澳维U20', '澳威北超', '澳昆U20', '澳维超', '澳维甲', '澳首超', '澳维女超', '澳新南联', '澳布女超']
	l6=['澳南女超', '日丙', '澳昆女超', '澳西超', '澳布超', '澳昆甲', '捷丙M', '捷丙', '沙滩足', '奥乙', '斯伐甲', '奥丙WT', '越南甲',  '澳昆超', '缅甸联', '德U19西', '波兰丁', '葡青A1北', '葡青A1南','', '波女超', '芬U20' ]
	l7=['丹麦乙A','英U23B', '芬女K联', '波兰乙',  '丹女超', '印尼超']
	listbxy.extend(l2)
	listbxy.extend(l3)
	listbxy.extend(l4)
	listbxy.extend(l5)
	listbxy.extend(l6)
	listbxy.extend(l7)
	#print(listbxy)
	list5=[]

	for x in iter(list2):
		#提出不需要的比赛
		if x[1]  in listbxy:continue
		if x[5]!='-':continue#未开场
		if x[9]!='半球':continue#半球
		list4=[]
		list4.append(x[1])
		list4.append(x[4])
		list4.append(x[6])
		list4.append(x[2])
		list4.append(x[5])
		list5.append(list4)
	#print(listbxy)	
	return list5


##球队名称对照整理
def dmdzb_zl():
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
			['墨西联春', '库里科', '尤尼昂', 'J联赛', '墨超', '库里科联队', '拉卡莱拉联合', '日职联'],
			['法乙', '巴黎足球会', '尼奥特', '02:00', '法乙', '巴黎FC', '尼奥特', '02:00'],
			['巴西甲', '巴拉纳竞技', '米内罗竞技', '06:00', '巴西甲', '巴拉纳竞技', '米涅罗竞技', '06:00'],
			['智利甲', '科金博', '库里科', '03:00', '智利甲', '科金博联队', '库里科联队', '03:00'],
			['俄甲', '伏尔加格勒', '辛历克', '23:00', '俄甲', '罗托伏尔加格勒', '辛历克', '23:00'],
			['巴西甲', '沙佩科恩斯', '奥瓦', '06:00', '巴西甲', '沙佩科恩斯', '阿瓦伊', '06:00'],
			['葡甲', '波尔图B队', '华森', '23:00', '葡甲', '波尔图B队', '瓦尔津', '23:00'],
			['俄甲', '诺夫哥罗德', 'SKA哈巴罗夫斯克', '22:00', '俄甲', '下诺夫哥罗德', 'SKA哈巴罗夫斯克', '22:00'],
			['俄甲', '希姆基', '下卡姆斯克石油', '22:00', '俄甲', '希姆基', '涅夫捷希米克', '22:00'],
			['乌克超', '柔亚', '亚历山德里亚', '00:30', '乌克超', '卢甘斯克黎明', '亚历山德里亚', '00:30'],
			['智利甲', '安托法加斯塔', '科布雷索', '03:00', '智利甲', '安托法加斯塔', '科布雷萨尔', '03:00']

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

	#整理结束

	return listdzb3

#球队名称对照
def dmdzb(name1,name2):

	listdzb3=dmdzb_zl()
	
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
	print("开始获取500万数据和球探数据....")
	listwbw=get500wzqdc(gethtmlsoup(''))

	#整理500万数据
	listwbw1=[]
	for wbw in listwbw:
		del wbw[3]
		listwbw1.append(wbw[0:5])
	#500万格式
	#['苏联杯', '邓迪FC', '阿伯丁', '22:00', '857652']
	
	listqt=getqtzqdc()
	print("球探数据")
	print(listqt)
	#球探数据格式
	#['比乙', '22:00', '圣吉罗斯', '洛克伦', '1-0']
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
	print("......比对结束.....")
	
	return listls



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
		#j=sjfenxClass(id1)
		#j.bd()
	
#测试。。。。。。。。。	
#dmdzb('','')
#获取半球盘的比赛id
#getqtzqdc()
li=(get_id_list(hb()))
wr_into_log(li)
