#from selenium.webdriver import Firefox
from selenium import webdriver
#from selenium.webdriver.firefox.options import Options


def main():
	#options = Options()
	#options.add_argument('-headless')
	url="http://odds.500.com/fenxi/ouzhi-806521.shtml"


	driver = webdriver.Firefox( )
	#driver.get("http://live.win007.com/index2in1.aspx?id=8")
	try:
		#driver.get(url)
		driver.get("http://www.baidu.com")
		print(driver.page_source)
		#tb1=driver.find_element_by_id("table_match")
		#tr=tb1.find_all('tr')
		#t=tb1.page_source
		#print (tr)

	except Exception as e:
		raise

	finally:
		driver.close()


if __name__ == '__main__':
	main()

