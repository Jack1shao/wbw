from gethtmlClass import getHtml
import re
#获取球探当日的比赛信息

h=getHtml()
t1=h.getHtml_by_firefox("http://live.win007.com/index2in1.aspx?id=8")
#print(t1)
li=re.findall('.*?([\u4E00-\u9FA5a-zA-Z0-9.:/()-]+)',t1)
list1=[]
list2=[]
for x in iter(li):

	list1.append(x)
	
	if x=='欧':list2.append(list1);list1=[]
	if x=='数据':list1=[]   
	if x==')':break;

list3=[]
for x in iter(list2):
	#同步开场未开场数据
	if x[3]=="-":x.insert(2,'0')
	#修复半场数据信息
	if not re.findall('-',x[6]):x.insert(6,'-')
	if x[9] in ['半球','受半球'] and x[2]=='0':list3.append(x);print(x)
#print(list3)
#for x in iter(li):	print(x)