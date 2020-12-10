#test
#	"python_interpreter":"D:/Anaconda3/envs/tensorflow/python.exe",


#
#from getjsbf import getjsbfClass
#from tooth_day import tooth_dayClass
#from htmlsoupClass import htmlsoup
#from zqconfigClass import zqconfigClass

#str_yestoday,str_sunday,str_saturday=tooth_dayClass(1).last_sunday_saturday()
#df=getjsbfClass(1).wcbf(str_sunday)
#print(abs(2-8)%2)
#from gethtmlClass import getHtml
#from htmlsoupClass import htmlsoup
#from sjfenxi import sjfenxClass
#from bs4 import BeautifulSoup
#from loggerClass import logger
#import re
#from zqconfigClass import zqconfigClass
#from tooth_day import tooth_dayClass
#from pandas.core.frame import DataFrame
#import tensorflow as tf
import numpy as np
def main():
	aa=[[[1,2,3],[2,4,5],[3,4,5],[4,4,5]],
		[[2,2,3],[2,4,5],[3,4,5],[4,4,5]],
		[[3,2,3],[2,4,5],[3,4,5],[4,4,5]],
		[[4,2,3],[2,4,5],[3,4,5],[4,4,5]],
		[[5,2,3],[2,4,5],[3,4,5],[4,4,5]],
		]


	ss=np.array(aa)
	print(ss.shape)
	pass
if __name__ == '__main__':
	main()