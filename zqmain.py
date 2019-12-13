#zqmain.py
#足球程序入口
from getjsbf import getjsbfClass
from zqconfigClass import zqconfigClass
from getzqClass import getzqClass
from tooth_day import tooth_dayClass
from buqisjClass import buqisj
from zqfenxi import zqfenxi
from fenxi2 import fenxi2

class zqmain(object):
	"""docstring for zqmain"""

	def __init__(self, arg):
		super(zqmain, self).__init__()
		self.arg = arg
	
	#昨日完场数据写入数据库

	def zrwc_save(self):
		kk=getjsbfClass(1)
		list_day=tooth_dayClass(1).last_sunday_saturday()
		li_wbw_wcbf=[]
		for d in list_day:

			li_wbw_wcbf.extend(kk.wcbf(d))
		if len(li_wbw_wcbf)==0:print('完场数据 have no date');return 0
		#读取联赛列表 from zqconfig
		zqdf=zqconfigClass('').cfg_select()
		li=zqdf.ls.values

		#in_500完场比赛 列表 
		id_wbw_wcbs=[(int(x[3])) for  x in li_wbw_wcbf if x[0] in li]
		kk=getzqClass('')

		#获取数据库中批量比赛id
		#list_idnm=[[]]
		list_idnm=kk.getbsid_bylist(id_wbw_wcbs)
		#二维转一维
		li_id=[]
		for li in list_idnm:
			for x in li:
				li_id.append(x)
		#数据库中没有的比赛id列表
		z=[id1 for id1 in id_wbw_wcbs if id1 not in li_id]
		print('数据库中没有的比赛id列表',z)
		z1=z[:10] if len(z)>10 else z
		print(z1,z)

		[getzqClass('').getbsid(idnm,idnm) for idnm in z if len(z)>0 ]
		
		return 1
	#获取比赛段的比赛数据
	#从config 文件获取比赛段
	def dwc_save(self):
		zqdf=zqconfigClass('').cfg_select()
		li=zqdf.values
		if len(li)==0:return 0
		print('..比赛段的比赛数据..')
		iii=0
		for idnm in li:
			if idnm[2]>0 and idnm[3]>0:
				iii+=getzqClass('').getbsid(idnm[2],idnm[3])
				if iii>19:
					print("--->{}<---".format(iii))
					break

		return 1
	#补齐整个联赛的比赛数据
	#从config 文件获取要补齐的联赛
	def lswc_save(self):
		zqdf=zqconfigClass('').cfg_select()
		li=zqdf.values
		ls=zqdf.ls.values
		if '英超' not in ls :print('12234556');return 0
		if len(li)==0:return 0
		iii=0
		for idnm in li:
			print(iii)
			if iii>60:break
			iii+=getzqClass('').getbs_othor(idnm[0],idnm[1])
		print("--->{}<---".format(iii))
		return 1
		

	#未开场数据分析
	def wkc_fenxi(self):
		kk=getjsbfClass(1)
		list_idnm=kk.jsbf2()

	#补齐必发数据
	def buqibf(self):
		h=buqisj('').bqbfmain(1,2)
		


	def main(self):
		i=0
		kk=zqfenxi(0)

		while i<5:
			i+=1

			print('\n<中文字幕:>\n')
			print('	1、获取完场比赛数据（昨日、上周六/上周日）  <1>')
			print('	2、分析未完场比赛数据                   <2>')
			print('	3、获取比赛段完场比赛数据和补齐联赛数据 <3 -33>')
			print('	4、补齐必发数据					<18>')
			print('	5、需获取比赛数据    					 <5>')
			print('	6、生成模型    					   <6>')
			print('	7、模型匹配  							<7>')
			print('	8、已有数据生成模型  					<8>')
			print('	91、取数据库，生成csv/菠菜公司  		<91>')
			print('	99、退出<99>\n')
			print('--请输入你的选择:')
			cc=input()
			if cc=='1':
				print('	1、获取完场比赛数据（昨日、上周六/上周日）<1>')
				self.zrwc_save()
			if cc=='2':
				print('	分析未完场比赛数据<2>')
				self.wkc_fenxi()
			if cc=='3':
				print('	补齐联赛数据<3>')
				self.lswc_save()
			if cc=='33':
				print('	获取比赛段完场比赛数据<33>')
				self.dwc_save()
			if cc=='18':
				print('补齐必发数据')
				self.buqibf()
			if cc=='5':
				print('5、需获取比赛数据')
				kk.get_bisai_df()
				kk.get_yjmx_idnm_list()
			if cc=='6':
				print('	6、生成模型       <6>')
				kk.add_mxk_wwcsj()
			if cc=='7':
				print('	7、模型匹配  		<7>')
			if cc=='8':
				print('	8、已有数据生成模型  		<8>')
				kk.fenxi_yysj()
			if cc=='91':
				kf=fenxi2(0).get_ouzhi_to_csv()

			if cc=='99':
				print('	退出<99>')
				break

#获取完场数据
h=zqmain(0).main()




