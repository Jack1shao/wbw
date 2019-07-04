#获取网页
from loggerClass import logger
import urllib.request
import random
import zlib
from chardet import detect
from bs4 import BeautifulSoup

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
class getHtml(object):
	"""docstring for getHtml
		获取网页,返回解码的网页信息
	"""
	#	
	def geturltext(self,url):

		# 
		header = {'Accept': "application/json, text/javascript, */*; q=0.01",
					'Accept-Language': 'en-US,en;q=0.8',
					'Cache-Control': 'max-age=0',
					'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
					'Connection': 'keep-alive',
					'Accept-Encoding':'gzip,deflate',
					'Referer': 'http://www.baidu.com/'
					}
		agentsList =[
						"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
						"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36",
						"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
						"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0"
					]
		#产生随机的User-agent
		ag=random.choice(agentsList)
		req = urllib.request.Request(url, headers=header)
		req.add_header('User-Agent',ag)
		try:
			reponse = urllib.request.urlopen(req)
			#print('get reponse')
		except urllib.error.URLError as e:
				print(e.reason)
				reponse.close()

		zobj = zlib.decompressobj(zlib.MAX_WBITS|16)
		decompressed_data = zobj.decompress(reponse.read())#压缩包解压，#print(reponse.info())查看
		#一定要关闭，不然会变为攻击

		reponse.close()
		#time.sleep(2+random.randint(0,6))
		codeing=detect(decompressed_data)#检测编码，	#print(codeing['encoding'])

		if codeing['encoding']=='GB2312':
			codes='gbk' #GB2312 转gbk
		else:
			codes=codeing['encoding']
		#转换编码
		#print('编码是',codes)
		htmlfile = decompressed_data.decode(codes)

		return htmlfile
	#
	def gethtml_by_selum(self,url):
		#print("get by selum")
		
		dcap = dict(DesiredCapabilities.PHANTOMJS)

		agentsList =[
							"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
							"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36",
							"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
							"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0"
					]
		#产生随机的User-agent
		ag=random.choice(agentsList)
		dcap["phantomjs.page.settings.userAgent"] = ag
		driver = webdriver.PhantomJS(desired_capabilities=dcap)
		try:
			driver.get(url)
			tb1=driver.find_element_by_id("table_live")
			t=tb1.text

		except Exception as e:
			raise

		finally:
			driver.close()
		
		#data=driver.page_source
		#print(data)
		#print(t)
		return   t

#测试类函数


#h=getHtml("http://live.win007.com/index2in1.aspx?id=8")	

#print(t1)