from gethtmlClass import getHtml
from htmlsoupClass import htmlsoup
#from sjfenxi import sjfenxClass
from bs4 import BeautifulSoup
from loggerClass import logger
import re
from zqconfigClass import zqconfigClass

from pandas.core.frame import DataFrame
class getjsbfClass(object):
	"""docstring for getjsbf"""
	def __init__(self, arg):
		super(getjsbfClass, self).__init__()
		self.arg = arg

	def _gethtmlsoup(self,url):
		#500w北单比方情况
		url="https://live.500.com/zqdc.php"
		
		#url="https://live.500.com/2h1.php"
		htmltext=getHtml().geturltext(url)
		soup=BeautifulSoup(htmltext,'lxml')
		return soup
	#500w北单比方情况
	#用find和get 获取数据
	def get500wzqdc(self,soup):
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
			#比分
			listbcbf=tdlist[8].get_text().split('-')
			#print(listbcbf)
			#list连接成一个
			listgy.extend(listsj)
			listgy.extend(idlist)
			#
			#if listbcbf[0]==' ':
			bsxxlist.append(listgy)
		return bsxxlist

		
	#获取昨日完场比分
	def get500wwcbf(self):
		print("获取500w比赛昨日完场比分数据")
		#url="https://live.500.com/wanchang.php"
		url='https://live.500.com/wanchang.php?e=2019-09-01'
		htmltext=getHtml().geturltext(url)
		soup=BeautifulSoup(htmltext,'lxml')
		listtable=soup.find_all(id='table_match')
		list31=listtable[0].find_all('tr')
		bsxxlist=[]
		#zqdf=zqconfigClass('').cfg_select()
		#li=zqdf.ls.values
		#print(li)

		for x in list31:
			#print(x)
			id12=(x.get('id'))
			if id12==None: continue
			#print(id12)
			id1=id12[1:]
			idlist=[]
			idlist.append(id1)	
			#获取联赛的球队
			listgy=(x.get('gy').split(','))

			#if listgy[0] not in li :continue
			#if listgy[0].find('女')>-1:continue
			#if listgy[0].find('U')>-1:continue
			#if listgy[0].find('丙')>-1:continue	
			listgy.extend(idlist)
			bsxxlist.append(listgy)
		#print(bsxxlist)	
		return bsxxlist
	#获取球探当日的比赛信息
	def getqtzqdc(self):
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
		#获取配置文件上的比赛列表
		#zqdf=zqconfigClass('').cfg_select()
		#li=zqdf.ls.values
		#
		list5=[]
		for x in iter(list2):
			#提出不需要的比赛
			#if x[1]  not in li:continue
			#if x[5]!='-':continue#未开场
			#if x[9]!='半球':continue#半球
			list4=[]
			list4.append(x[1])
			list4.append(x[4])
			list4.append(x[6])
			list4.append(x[2])
			list4.append(x[5])
			list4.append(x[9])
			list5.append(list4)
	
		return list5


	##球队名称对照整理
	def _dmdzb_zl(self,bz):
		listdzb=[
				['内卡萨', '森索罗', '摩斯高伦', 'SJK', '拿加沙', '萨索洛', '穆斯克龙', '塞那乔其'] ,
				['达尔库尔德', '唐迪拉', '年轻人', '谢周三', '达尔科德', '通德拉', '年青人', '谢菲尔德星期三'] ,
				['欧帕尔利奥', '奎尔巴', '厄斯特松德', '科布雷索', '蓬塔格罗萨铁路工人', '库亚巴', '奥斯特桑斯', '科布雷萨尔'] ,
				['卢甘斯克黎明', '下卡姆斯克石油', '下诺夫哥罗德', '华森', '柔亚', '涅夫捷希米克', '诺夫哥罗德', '瓦尔津'] ,
				['奥瓦', '伏尔加格勒', '科金博', '米内罗竞技', '阿瓦伊', '罗托伏尔加格勒', '科金博联队', '米涅罗竞技'] ,
				['巴黎FC', 'J联赛', '尤尼昂', '库里科', '巴黎足球会', '日职联', '拉卡莱拉联合', '库里科联队'] ,
				['墨西联春', '蒙特瑞', 'CSA阿拉戈诺', '保地花高SP', '墨超', '蒙特雷', '阿拉戈亚诺体育队', '博塔弗戈SP'] ,
				['厄勒布鲁', 'K1联赛', '欧罗巴杯', '亚拉腊亚美尼亚', '奥雷布洛', '韩K联', '欧罗巴联赛', '阿拉特阿美尼亚'] ,
				['提华纳', '欧冠杯', '米内罗美洲', 'J2联赛', '蒂华纳', '欧冠联赛', '米涅罗美洲', '日职乙'] ,
				['山口雷法', '古拉瑞奇', '自由杯', '漫游者(中)', '山口雷诺法', '库卡瑞奇', '解放者杯', '蒙得维的亚流浪者'] ,
				['比尔舒华夏普尔', '南俱杯', '里加', '奥斯杰克', '贝尔谢巴夏普尔', '南球杯', '里加FC', '奥西耶克'] ,
				['奥斯纳布吕克', '奥兰斯', '尚布利', '兹沃勒', '奥斯纳布鲁克', '奥尔良', '查布莱', '泽沃勒'] ,
				['PAOK塞萨洛尼基', '卡拉巴克', '隆德里纳', '华沙军团', '塞萨洛尼基', '卡拉巴赫', '隆迪那', '华沙莱吉亚'] ,
				['博莱斯拉夫', '北雪平', '布加勒斯特星(中)', 'U康塞普森', '博雷斯拉夫', '诺科平', '布加勒斯特星队', '康塞普西翁大学'] ,
				['赫尔蒙德', '阿贾克斯B队', '丹超', '兰德斯', '赫尔蒙特', '阿贾克斯青年队', '丹麦超', '兰讷斯'],
				['葡超', '辛达卡拉', '比兰尼塞斯', '00:00', '葡超', '圣塔克拉拉', '比兰尼塞斯', '23:59'],
				['冰岛超', '维京古', '格林达维克', '03:15', '冰岛超', '维京古尔', '格林达维克', '03:15'],
				['挪甲', 'KFUM奥斯陆', 'UII奇萨', '23:59', '挪甲', 'KFUM奥斯陆', '基萨', '00:00'],
				['挪甲', '松达尔', '康斯文格', '23:59', '挪甲', '松达尔', '孔斯温厄尔', '00:00'],
				['挪超', '莫尔德', '奥德格伦兰', '23:59', '挪超', '莫尔德', '奥德', '00:00'],
				['挪超', '基斯迪辛特', '莫达伦', '23:59', '挪超', '克里斯蒂安松', '莫达伦', '00:00'],
				['俄超', '罗斯托夫', '喀山鲁宾', '23:59', '俄超', '罗斯托夫', '喀山红宝石', '00:00']

				]
		#整理
		listzl=[]
		for li in listdzb:
			for x in range(0,4):
				
				if li[x]==li[x+4]:continue
				list11=[]
				list11.append(li[x])
				list11.append(li[x+4])
				list11.sort()
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
		if bz==1:
			[print(li,',') for li in listdzb3 if 1==1]

		#整理结束

		return listdzb3

	#球队名称对照
	def dmdzb(self,name1,name2,listdzb3):

		#listdzb3=self._dmdzb_zl(0)
		#df=zqconfigClass(0).cfg_dmdzb_select()
		#listdzb3=df.values
		#名字相等
		if name1==name2:return 1
		#名字在对照表中
		#print(name1,name2,levle)
		for x in listdzb3:
			for xx in range(0,4):
				if  x[xx]==name1 and x[xx+4]==name2:return 1
				if  x[xx]==name2 and x[xx+4]==name1:return 1
		return 0


	def hb(self):
		print("开始获取500万数据和球探数据....")
		listwbw=self.get500wzqdc(self._gethtmlsoup(''))

		#整理500万数据
		listwbw1=[]
		for wbw in listwbw:
			del wbw[3]
			listwbw1.append(wbw[0:5])

		#500万格式
		#['苏联杯', '邓迪FC', '阿伯丁', '22:00', '857652']
		print("球探数据")
		listqt1=self.getqtzqdc()
		listqt=[]
		for x in listqt1:
			if x[0].find('女')>-1:continue
			if x[5]=='半球':
				print(x)
				listqt.append(x)

		#
		cfg=zqconfigClass(1)
		df=cfg.cfg_dmdzb_select()
		listdzb3=df.values
		#球探数据格式
		#['比乙', '22:00', '圣吉罗斯', '洛克伦', '1-0']
		listls=[]
		list_fz=[]
		for qt in listqt:
			for wbw in listwbw1:
				#if qt[3]!=wbw[3]:break#比赛时间相等
				bz=1
				#队名和比赛时间相等
				for x in range(0,4):
					bz=bz*self.dmdzb(qt[x],wbw[x],listdzb3)
				if bz:
					listls.append(wbw)
					break

				#辅助对照

				if bz==0 and self.dmdzb(qt[3],wbw[3],listdzb3) and self.dmdzb(qt[0],wbw[0],listdzb3) and (self.dmdzb(qt[1],wbw[1],listdzb3) or self.dmdzb(qt[2],wbw[2],listdzb3)):

					print("辅助对照：")
					l1=[]
					l2=[]
					for x in range(0,4):
						l2.append(wbw[x])
						l1.append(qt[x])
					l1.extend(l2)
					print(l1)
					list_fz.append(l1)
		if len(list_fz)>0:
			df1=DataFrame(list_fz,columns=['n1','n2','n3','n4','n5','n6','n7','n8'])		
			cfg.cfg_dmdzb_append(df1,'zqconfig_dmdzb.csv') 
		print("比对结果：")		
		for x in listls:
			print(x)
		print("......比对结束.....")
		
		return listls



	#获取半球的id号
	def get_id_list(self,datlist):
		idlist=[]
		for li in datlist:
			idlist.append(li[4])
		return idlist
		

	#写入文件
	def wr_into_log(self,datlist):
		lg=logger()
		lg.info(datlist)
		for x in datlist:
			id1=int(x)
			#j=sjfenxClass(id1)
			#listret,res=j.bd()
			#lg.info(listret)
			#lg.info(res)
#k=getjsbfClass(0)
#if k.arg==0:

#测试。。。。。。。。。	
#dmdzb('','')
#获取半球盘的比赛id
#getqtzqdc()
#kk=getjsbfClass()
#kk.get500wwcbf()
#li=(get_id_list(hb()))
#wr_into_log(li)
#bz=0
#dmdzb_zl(0)
