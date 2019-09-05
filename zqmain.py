#zqmain.py
#足球程序入口
from getjsbf import getjsbfClass
from zqconfigClass import zqconfigClass
from getzqClass import getzqClass
class zqmain(object):
	"""docstring for zqmain"""

	def __init__(self, arg):
		super(zqmain, self).__init__()
		self.arg = arg
	
	#昨日完场数据写入数据库

	def zrwc_save(self):
		kk=getjsbfClass(1)
		li_wbw_wcbf=kk.get500wwcbf()
		if len(li_wbw_wcbf)==0:print('完场数据 have no date');return 0
		#读取联赛列表 from zqconfig
		zqdf=zqconfigClass('').cfg_select()
		li=zqdf.ls.values

		#in_500完场比赛 列表 
		id_wbw_wcbs=[(int(x[3])) for  x in li_wbw_wcbf if x[0] in li]
		kk=getzqClass('')

		#获取数据库中批量比赛id
		list_idnm=kk.getbsid_bylist(id_wbw_wcbs)
		#二维转一维
		li_id=[]
		for li in list_idnm:
			for x in li:
				li_id.append(x)
		#数据库中没有的比赛id列表S
		z=[id1 for id1 in id_wbw_wcbs if id1 not in li_id]
		print('数据库中没有的比赛id列表',z)
		[getzqClass('').getbsid(idnm,idnm) for idnm in z if len(z)>0]
	
		return 1
	#未开场数据分析
	def wkc_fenxi(self):
		kk=getjsbfClass(1)
		list_idnm=kk.hb()

#获取完场数据
h=zqmain(0)
#if h.arg==0:h.zrwc_save()
h.wkc_fenxi()


