#test
#

#
from getjsbf import getjsbfClass
from tooth_day import tooth_dayClass
from htmlsoupClass import htmlsoup
from zqconfigClass import zqconfigClass

#str_yestoday,str_sunday,str_saturday=tooth_dayClass(1).last_sunday_saturday()
#df=getjsbfClass(1).wcbf(str_sunday)
zqdf=zqconfigClass('').cfg_select()
li=zqdf.values
print(li)

