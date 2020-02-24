#test
#

#
from getjsbf import getjsbfClass
from tooth_day import tooth_dayClass
from htmlsoupClass import htmlsoup

#str_yestoday,str_sunday,str_saturday=tooth_dayClass(1).last_sunday_saturday()
#df=getjsbfClass(1).wcbf(str_sunday)
def getbs():
	print('开始获取')
	id1=808418
	hs=htmlsoup(id1)

	scblist,bzsc,ozlist=hs.getscbandouzhi()

getbs()

