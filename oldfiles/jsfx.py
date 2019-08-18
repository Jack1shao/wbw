import get500w1
from bs4 import BeautifulSoup


def test(url0):
	url0='http://live.500.com/zqdc.php'
	htmltext=get500w1.geturltext(url0)
	soup=BeautifulSoup(htmltext,'lxml')

	list3=soup.find_all(id='table_match')
	print(len(list3))

	list31=list3[0].find_all('input')
	for x in list31:
		print(x.get('value'))
		pass
	#htmlsoup=get500w1.gethtmlsoup(get500w1.geturltext(url0))
	#BeautifulSoup
	#
	#page=get500w1.gethtmlsoup(get500w1.selum(url0))
	#print(page.find_all('input').get('value'))

	
	#print(page.input)
	#print(htmlsoup.title)
	return 0


test('')