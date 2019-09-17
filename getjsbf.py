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
		htmltext=getHtml().getHtml_by_firefox(url)
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



	def wcbf(self,day):
		url1="https://live.500.com/wanchang.php"
		url2='?e={}'.format(day)
		url=url1+url2
		print(url)
		return self.get500wwcbf(url)
		
	#获取昨日完场比分
	def get500wwcbf(self,url):
		print("获取500w比赛昨日完场比分数据")
		#url="https://live.500.com/wanchang.php"
		#url='https://live.500.com/wanchang.php?e=2019-09-01'
		htmltext=getHtml().getHtml_by_firefox(url)
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



	#球队名称对照
	def dmdzb(self,name1,name2,listdzb3):
		#listdzb3为对照表
		#名字相等
		if name1==name2:return 1
		#名字在对照表中
		for x in listdzb3:
			for xx in range(0,4):
				if  x[xx]==name1 and x[xx+4]==name2:return 1
				if  x[xx]==name2 and x[xx+4]==name1:return 1
		return 0

	#获取即时比分
	def jsbf(self):
		
		print("\n.....................开始获取即时比分数据.....................")
		
		print("\n1.获取500万数据")
		listwbw=self.get500wzqdc(self._gethtmlsoup(''))
		#整理500万数据
		listwbw1=[]
		for wbw in listwbw:
			del wbw[3]
			listwbw1.append(wbw[0:5])
		#500万格式
		#['苏联杯', '邓迪FC', '阿伯丁', '22:00', '857652']

		print("\n2.获取球探数据")
		listqt1=self.getqtzqdc()
		listqt=[]
		for x in listqt1:
			if x[0].find('女')>-1:continue
			if x[0].find('丙')>-1:continue
			if x[0].find('丁')>-1:continue


			if x[5]=='半球':
				print('--------------->>',x)
				listqt.append(x)
		#获取对照表
		cfg=zqconfigClass(1)
		df=cfg.cfg_dmdzb_select()
		listdzb3=df.values
		#球探数据格式
		#['比乙', '22:00', '圣吉罗斯', '洛克伦', '1-0']
		listls=[]
		list_fz=[]
		for qt in listqt:
			for wbw in listwbw1:
				bz=1
				#队名和比赛时间相等
				for x in range(0,4):
					bz=bz*self.dmdzb(qt[x],wbw[x],listdzb3)
				if bz:
					listls.append(wbw)
					break

				#辅助对照
				if bz==0 and self.dmdzb(qt[3],wbw[3],listdzb3) and self.dmdzb(qt[0],wbw[0],listdzb3) and (self.dmdzb(qt[1],wbw[1],listdzb3) or self.dmdzb(qt[2],wbw[2],listdzb3)):
					print("\n@@辅助对照：")
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
		
		print("\n-----------------------比对结果：写入config文件---------------\n")		
		if len(listls)>0:	
			#['欧洲杯', '德国', '荷兰', '02:45', '793185']
			df1=DataFrame(listls,columns=['ls','zd','kd','bssj','idnm'])
			files1='zqconfig_bslb.csv'
			cfg.append(df1,files1)#写入文件
		for x in listls:
			print(x)
		print("\n------------------------------比对结束-------------------------\n")
		
		#清理
		listls.clear()
		list_fz.clear()
		listqt.clear()
		listwbw.clear()
		listwbw1.clear()
		return 0
	#获取要分析的比赛列表
	def get_id_list(self):
		h=zqconfigClass(0)
		df=h.select('zqconfig_bslb.csv')
		#print(df.idnm.values)
		return df.idnm.values.tolist()
	#返回df
	def get_df(self,list1):
		li=self.get_id_list()
		print(li)
		k=htmlsoup(0)
		iii=0
		for x in li:
			iii+=1
			if iii>1:break
			k=htmlsoup(x)
			scblist,z,ouzhilist=k.getscbandouzhi()
			columns_list_ouzhi=['idnm', 'xh', 'bcgs', 'cz3', 'cz1', 'cz0', 'jz3', 'jz1', 'jz0', 'cgl3', 'cgl1', 'cgl0', 'jgl3', 'jgl1', 'jgl0', 'chf', 'jhf', 'ck3', 'ck1', 'ck0', 'jk3', 'jk1', 'jk0']
			df=DataFrame(ouzhilist,columns=columns_list)
			print(df.head())
		return df
#columns_list_scb= ['idnm', 'zd', 'kd', 'nd', 'ls', 'lc', 'zjq', 'kjq', 'bstime']
#columns_list_bifa=['idnm', 'xh', 'xm', 'pl', 'gl', 'bd', 'bf', 'cjj', 'cjl', 'zjyk', 'bfzs', 'lrzs', 'ykzs']


#测试。。。。。。。。。	
#k=getjsbfClass(0)
#k.get_df(k.get_id_list())

