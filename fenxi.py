
import mysql_cmd
import excle_cmd


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

def ouzhi_fenxi(dateList1):
	list3=[]
	y=len(dateList1)
	if y==0:
		print('没有欧指数据返回0')
		return 0
	ms=[' ',' ',' ',' ',' ',' ','*']
	bz=0
	bb1=0
	for x in dateList1:

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
		


		# if(abs(c3)-abs(j3)<0):
		# 	ms.append('3偏离')
		# 	#print("3偏离"+x[2]+'--',float('%.4f'%j3))
		# if(abs(c1)-abs(j1)<0 and j1-jf>0.03):
		# 	ms.append('1偏离')
		# 	#print("1偏离"+x[2]+'--',float('%.4f'%j1))
		# if(abs(c0)-abs(j0)<0):
		# 	ms.append('0偏离')
		# 	
		if x[2]=='Bet365':bb1=int(x[3]-x[4])
		
		if jk1==ck1 and x[2]=='威廉希尔' :
			del ms[0]
			ms.insert(0,'威廉希尔平赔付不变')
			bz=1

		if x[2]=='威廉希尔'  and jk1>0.99:
			del ms[0]
			ms.insert(0,'高企威廉平赔付')
			bz=1

		if(x[2]=='威廉希尔' and  ck1<cf+0.010 and ck1>cf-0.070 and jk1>=1 and jk1!=ck1):
			a=ms[0]
			del ms[0]
			ms.insert(0,'@高企平赔'+a)#平赔高企
			bz=1



		if jk1==ck1 and x[2]=='Bet365' :
			del ms[1]
			ms.insert(1,'bet365平赔付不变')
			bz=1
		if jk1==ck1 and (x[2]=='立博' ):
			del ms[2]
			ms.insert(2,'立博平赔付不变')
			bz=1

		if x[2]=='Bet365' and (jk3>0.99 or jk0>0.99):
			del ms[3]
			if jk3>jk0:
				str2='jk3'
			else:
				str2='jk0'
			print(jk3,jk1,jk0,cf,jf)
			ms.insert(3,'Bet365的'+str2+'大于1'+'j1='+str(j1))#高位扩展
			bz=1			


		if (x[2]=='Bet365' and ((ck3>1 and jk3>jf+0.02) or (ck0>1 and jk0>jf+0.02))):
			del ms[4]
			ms.insert(4,'bet365 高位不降')
			bz=1

		if x[2]=='Bet365' and ((ck3<cf-0.1 and jk3>=1) or (ck0<cf-0.1 and jk0>=1)):
			del ms[4]
			if jk3>jk0:
				str2='jk3'
			else:
				str2='jk0'
			ms.insert(4,'bet365高低刷 '+str2)
			bz=1	
		if x[2]=='Bet365' and ck1<cf+0.01 and jk1>0.99:
			del ms[1]
			ms.insert(1,'@高企bet365平赔付')
			bz=1
		if x[2]=='BINGOAL' and (jk0>0.99 or jk3>0.99):
			del ms[5]
			ms.insert(5,'BINGOAL赔付高企')
			bz=1
		if x[2]=='Bet365' and ck1==jk1 and ((ck0==jk0 and ck3!=jk3) or (ck0!=jk0 and ck3==jk3)) :
			del ms[4]
			ms.insert(4,'bet365平赔付,独变')
			bz=1
		if x[2]=='Expekt' and ((ck3<cf-0.1 and jk3>=1) or (ck0<cf-0.1 and jk0>=1)):
			del ms[6]
			ms.insert(6,'Expekt高低刷')
			bz=1
	if bz==1 or bz==0:
		list3.append(dateList1[0][0])
		list3.append(bb1)
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
	print(len(dateList1))
	for x in dateList1:
		list1=[]
		
		
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
			oz1.append(bsxxlist[0][3]+bsxxlist[0][4])
		oz1.append(x[4]+'--'+x[7])
		print(oz1)
		jglist.append(oz1)

	excle_cmd.ctrl_excel.write_excel(jglist)
	#print(jglist)
	return dateList1

fenxi1('半球','')