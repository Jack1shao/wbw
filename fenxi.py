
import mysql_cmd
import excle_cmd
import datetime


#获取一个比赛信息
def getbsx_by_id(idnm):

	sql="select * from scb where idnm="+str(idnm)
	dateList1=mysql_cmd.mysql_cmd1.selectMysql(sql)
	
	return dateList1


def getouzhi_by_id(idnm):
	sql="select * from ouzhi where idnm="+str(idnm)
	dateList1=mysql_cmd.mysql_cmd1.selectMysql(sql)
	
	return dateList1

def  getyapan_by_id(idnm):
	sql="select * from yapan where idnm="+str(idnm)
	dateList1=mysql_cmd.mysql_cmd1.selectMysql(sql)
	
	return dateList1

#3个数最大值
def get_max(list1):
	#list1=[['jk3',0.98],['jk1',0.92],['jk0',0.96]]
	list2=[]
	bz=''
	for x in list1:
		if x[1]==max([list1[0][1],list1[1][1],list1[2][1]]):
			bz=x[0]+bz
			list2.append(x)
	print(list2)
	return list2

#判断是否交叉盘
def is_jcp(id1):
	sql="select Y.idnm,Y.bstime,(SELECT c.jp from yapan c where c.idnm=y.idnm and c.ypgs='Bet365') FROM scb y where (y.lc,y.nd,y.ls) in (select a.lc,a.nd,a.ls from scb a where a.idnm="+str(id1)+")"
	list1=mysql_cmd.mysql_cmd1.selectMysql(sql)
	#print(list1)
	jp=''
	bstime=''
	bz=''
	#print(len(list1))
	for x in list1:
		if x[0]==id1:
			jp=x[2]
			bstime=x[1]
	
	bst1 = datetime.datetime.strptime(bstime, "%Y-%m-%d %H:%M")
	#10小时之内的比赛
	tend=(bst1+datetime.timedelta(hours=10))
	tstart=(bst1+datetime.timedelta(hours=-10))
	
	for x in list1:
		if x[2]==jp and x[0]!=id1:
			t=datetime.datetime.strptime(x[1], "%Y-%m-%d %H:%M")
			#10小时之内的比赛
			if t>tstart and t<tend:
				bz='交叉盘' #bz=1 为交叉盘
	#print(bz)	
	return bz

def ouzhi_fenxi(dateList1):
	list3=[]
	y=len(dateList1)
	if y==0:
		print('没有欧指数据返回0')
		return 0
	ms=['','','','','','']
	bz=0
	bb1=0
	bocailist=['Bet365','Oddset','Iceland','威廉希尔','BINGOAL','Sweden','Betshop','Expekt','立博']
	listIceland=[]
	listBINGOAL=[]
	listExpekt=[]
	listSweden=[]
	listWill=[]
	listLibo=[]
	listBet365=[]
	listOddset=[]

	for x in dateList1:
		if x[2] not in bocailist:
			continue
		#初赔返还率
		cf=float(x[15]/100)
		#即时赔返还率
		jf=float(x[16]/100)
		
		#凯利指数
		ck3=float(x[17])
		ck1=float(x[18])
		ck0=float(x[19])
		jk3=float(x[20])
		jk1=float(x[21])
		jk0=float(x[22])
		#凯利与返还率的差值
		c3=ck3-cf
		c1=ck1-cf
		c0=ck0-cf
		j3=jk3-jf
		j1=jk1-jf
		j0=jk0-jf

		#赔付最远值
		# listj=[['j3',abs(j3)],['j1',abs(j1)],['j0',abs(j0)]]
		# maxj=get_max(listj)
		#print(maxj)
		listbs=''
		if jk3>=jk1 and jk3>=jk0:listbs='jk3最大值 '
		else:
			if jk3>jf:listbs='jk3大于返还率 '

		
		str1=''
		if ck3>0.99:str1='ck3 '+str1
		if ck0>0.99:str1='ck0 '+str1
		if jk1>0.99:str1='jk1 '+str1
		if ck1>0.99:str1='ck1 '+str1
		if jk3>0.99:str1='jk3 '+str1
		if jk0>0.99:str1='jk0 '+str1
			
		#Bet365
		if x[2]=='Bet365':
			
			# if(abs(c3)-abs(j3)<-0.01) and x[2]=='Bet365':
			# 	ms.append('3偏离'+str(jk3))
			# else:
			# 	ms.append('')
			
			# if abs(c1)-abs(j1)<-0.01  and x[2]=='Bet365':
			# 	ms.append('1偏离')
			# else:
			# 	ms.append('')
			
			# if(abs(c0)-abs(j0)<-0.01) and x[2]=='Bet365':
			# 	ms.append('0偏离')
			# else:
			# 	ms.append('')

			if jk1==ck1 :
				del ms[2]
				ms.insert(2,'bet365平赔付不变')
				bz=1
			if x[2]=='Bet365' and ck1<cf+0.01 and jk1>0.99:
				del ms[2]
				ms.insert(2,'@高企bet365平赔付')
				bz=1

			# if x[2]=='Bet365' and (jk3>0.99 or jk0>0.99):
			# 	del ms[3]
			# 	if jk3>jk0:
			# 		str2='jk3'
			# 	else:
			# 		str2='jk0'
				
			# 	ms.insert(3,'Bet365的'+str2+'大于1')#高位扩展
			# 	bz=1

			if ck1==jk1 and ((ck0==jk0 and ck3!=jk3) or (ck0!=jk0 and ck3==jk3)) :
				del ms[3]
				ms.insert(3,'bet365独变其中一个赔率')
				bz=1			

			if (x[2]=='Bet365' and ((ck3>1 and jk3>jf+0.02) or (ck0>1 and jk0>jf+0.02))):
				del ms[3]
				ms.insert(3,'bet365 高位不降')
				bz=1

			if x[2]=='Bet365' and ((ck3<cf-0.1 and jk3>=1) or (ck0<cf-0.1 and jk0>=1)):
				del ms[3]
				if jk3>jk0:
					str2='jk3'
				else:
					str2='jk0'
				ms.insert(3,'bet365高低刷 ')
				bz=1


		

		#威廉希尔
		if (ck3>0.99 or ck0>0.99 or jk1>0.99) and x[2]=='威廉希尔' :

			del ms[0]
			ms.insert(0,'威廉付赔'+str1)
			bz=1

		if (ck3>0.99 or ck0>0.99 or jk1>0.99) and x[2]=='立博' :

			del ms[1]
			ms.insert(1,'立博付赔'+str1)
			bz=1
		
		# if jk1==ck1 and (x[2]=='立博' ):
		# 	del ms[2]
		# 	ms.insert(2,'立博平赔付不变')
		# 	bz=1

		# if x[2]=='BINGOAL' and (jk0>0.99 or jk3>0.99):
		if x[2]=='BINGOAL':
			del ms[5]
			ms.insert(5,'BINGOAL赔付'+str1)
			bz=1

		# if x[2]=='Expekt' and ((ck3<cf-0.1 and jk3>=1) or (ck0<cf-0.1 and jk0>=1)):
		if x[2]=='Expekt' :
			del ms[4]
			ms.insert(4,'Expekt '+str1)
			bz=1
		if x[2] in ['Iceland','Sweden','Oddset']:
			ms.append(x[2]+listbs)
		#if x[2]=='Sweden':ms.append(listbs)
	
	print(len(ms))
	
	for x in range(9-len(ms)):
		ms.append('')
	print(len(ms))
	if bz==1 or bz==0:
		list3.append(dateList1[0][0])
		
		for x in ms:
			list3.append(x)

	return list3

def  fenxi1(jp,cp):

	if cp.strip()!='':
		str1=" and cp='"+str(cp)+"'"
	else:
		str1=''

	sql="select * from yapan  where ypgs='Bet365' and jp='"+str(jp)+"'" +str1
	dateList1=mysql_cmd.mysql_cmd1.selectMysql(sql)
	jglist=[]
	#print(len(dateList1))
	for x in dateList1:
		list1=[]
		idnm=x[0]
		#print(idnm)
		#取欧指数据
		ouzhilist=getouzhi_by_id(x[0])
		#print(ouzhi_fenxi(ouzhilist))
		# 
		# #取比赛结果、进球差
		oz1=ouzhi_fenxi(ouzhilist)
		#print(oz1)
		bsxxlist=getbsx_by_id(oz1[0])
		#print(bsxxlist)
		if len(bsxxlist)>0:
			oz1.append(bsxxlist[0][1]+'vs'+bsxxlist[0][2])
			oz1.append(bsxxlist[0][6]-bsxxlist[0][7])
			oz1.append(bsxxlist[0][3]+bsxxlist[0][4]+str(bsxxlist[0][5]))
		oz1.append(x[4]+'--'+x[7])
		oz1.append(is_jcp(idnm))
		print(oz1)
		jglist.append(oz1)

	excle_cmd.ctrl_excel.write_excel(jglist)
	#print(jglist)
	return dateList1

fenxi1('半球','')
#
#is_jcp(673112)
#get_max('')