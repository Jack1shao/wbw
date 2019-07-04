
##网页解析
from gethtmlClass import getHtml
from bs4 import BeautifulSoup
import re
import io
class htmlsoup(object):
	"""docstring for htmlsoup
		##网页解析
	"""
	def __init__(self, arg):
		super(htmlsoup, self).__init__()
		self.arg = arg
		self.idnm=arg
		

	def _gethtmlsoup(self,url):
		htmltext=getHtml().geturltext(url)
		soup=BeautifulSoup(htmltext,'lxml')
		return soup


	def _set_sc_url_soup(self,starts):
		url="http://odds.500.com/fenxi1/ouzhi.php?id={}&ctype=1&start={}&r=1&style=0&guojia=0&chupan=1".format(self.idnm,starts)
		id1=self.idnm
		return self._gethtmlsoup(url),id1
	def _set_yapan_soup(self):
		url="http://odds.500.com/fenxi/yazhi-{}.shtml?ctype=2".format(self.idnm)
		id1=self.idnm
		return self._gethtmlsoup(url),id1
	def _set_bifa_soup(self):
		url="https://odds.500.com/fenxi/touzhu-{}.shtml".format(self.idnm)
		id1=self.idnm
		return self._gethtmlsoup(url),id1
		

	#返回赛程表
	def getsc(self):
		#返回数据列表
		datalist=[]

		soup,id1=self._set_sc_url_soup(0)
		soupdz=soup.find_all('a','hd_name')
		#判断数据，返回空
		if len(soupdz)!=3:return datalist,0
		#创建比赛信息列表
		bsxxlist=[]
		bsxxlist.append(str(id1))
		bsxxlist.append(soupdz[0].text.strip())
		bsxxlist.append(soupdz[2].text.strip())

		str11=soupdz[1].text.strip()
		#取年份
		bsxxlist.append(str11[0:2])

		#去掉‘第’字。联赛
		ls=re.findall('.*?([\u4E00-\u9FA5]+)',str11)
		bsxxlist.append(ls[0][0:-1])
		print(str11[-3:],str11)

		#获取轮次
		lun=re.findall('\d+',str11[-3:])
		if len(lun)>0:bsxxlist.append(lun[0])
		else:bsxxlist.append('-1')

		#获取比分
		soupbf=soup.find('p','odds_hd_bf')
		jqs=re.findall('\d+',soupbf.text)
		if len(jqs)==0:
			bsxxlist.append('-100')
			bsxxlist.append('-1000')
		else:
			[bsxxlist.append(x) for x in jqs]
			
		#获取比赛时间
		souptime=soup.find('p','game_time')
		bsxxlist.append(souptime.text.strip('比赛时间'))
		print(bsxxlist)
		
		datalist.append(bsxxlist)
		return datalist,1


	#获取欧赔公司数量
	#return int
	def _getbcgscount(self,soup):
		souphtml=soup.find_all(id='nowcnum')
		cnum=re.findall('\d+',souphtml[0].text)
		a=int(cnum[0])-2
		return a

	#解析网页文本,获取500W欧指
	# return list
	def _ansy_500wouzhi(self,id1,soup):
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

	#返回欧指
	def getouzhi(self):
		print("获取  {}  500W欧指".format(self.idnm))
		datalist=[]
		souplist=[]
		soup,id1=self._set_sc_url_soup(0)
		tbsoup=soup.find_all(id='table_cont')
		if len(tbsoup)==0:return datalist,0
		datalist+=self._ansy_500wouzhi(id1,soup.find_all(id='table_cont'))

		a=self._getbcgscount(soup)-1
		for x in range(int(a/30)):
			
			starts=30*(x+1)
			soup2,id2=self._set_sc_url_soup(starts)
			aalist=self._ansy_500wouzhi(id1,soup2)
			if len(aalist)==0 and id1!=id2: return datalist,0
			datalist+=aalist

		return datalist,1

	def getyapan(self):
		list3=[]
		soup,id1=self._set_yapan_soup()
		souplist=soup.find_all(id='table_cont')
		if len(souplist)==0:return list3,0
		yclist=['主', '客', '同','升', '(优胜客)','(明升)','降','(壹貳博)','(沙巴)','(乐天堂)','(大发)']
		y=0
		bz=8
		
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
			# if lenlist2%bz==0:
			if 1:
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
		
		return list3,1
		

	def getbifa(self):
		print("获取  {}  必发数据".format(self.idnm))
		soup,id1=self._set_bifa_soup()
		ss=soup.find_all('table')
		print(len(ss))
		listbifa=[]
		for tb in ss[6:10]:
			row=tb.find_all("tr")
			for cell in row:
				cc=cell.find_all('td')
				for x in cc:
					#print(x.text)
					listbifa.append(x.text)
					if x.text=='盈亏指数':listbifa=[]
		llli=[]			
		for li in iter(listbifa):
			llli.append(li)
			if li=='平局':llli=[]
			
		print(llli)
		print(listbifa)

		pass


h=htmlsoup(780288)
print(h.getbifa())