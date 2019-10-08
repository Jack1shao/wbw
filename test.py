
import itertools

import time,datetime
from pandas.core.frame import DataFrame
from functools import reduce
import pandas as pd
import pymysql
from loggerClass import logger
import urllib.request
import random
import zlib
from chardet import detect
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import os
from zqconfigClass import zqconfigClass
from tooth_excle import tooth_excleClass

#获取上个周六，周日
#如果今日非周六，周日
def last_sunday_saturday():
	#获取上个周六，周日
	#如果今日非周六，周日
	date=datetime.datetime.now()
	day = date.weekday()

	if day<5:
		saturday=date+datetime.timedelta(days=-day-2)
		sunday=date+datetime.timedelta(days=-day-1)
		str_sunday=sunday.strftime('%Y-%m-%d')
		str_saturday=saturday.strftime('%Y-%m-%d')
	return str_sunday,str_saturday

def li_kz(li1,li2):

	li_ret=[]
	for i1 in li1:
		li=[]
		li.append(i1)
		l=set(li)
		if l not in li_ret:
			li_ret.append(l)
	print(li_ret)		
	return li_ret

def li_kz2(li1,li2):
	li_ret=[]
	code=','
	#z=[str(i1)+code+str(i2) for i1 in li1 for i2 in li2  ]
	#for i in itertools.product(li1,repeat=6):
		#print(DataFrame(i))
	fn = lambda x, y: reduce(lambda x, y: [str(i)+code+str(j) for i in x for j in y], x)
	#print(fn(x,code))		
	fn=lambda x, y: [str(i)+code+str(j) for i in x for j in y if str(i)!=str(j)]
	#z=reduce(lambda x, y: x+y, [1,2,3,4,5])
	#z=reduce(fn(li1,li2),[1,2,3,4,5])
	z=fn(li1,li2)
	z=fn(z,li1)
	print(z)
	return 0

def list_in(*li):
	iii=0
	for i in li:
		iii+=1
		print(iii,i)
	return 0

def read_sql():
	pass
	conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='mysql',port=3306,charset='utf8')
	#charset用于修正中文输出为问号的问题
	sql = "select * from yapan where idnm=784159"
	df = pd.read_sql(sql, conn)
	print(df.columns.values.tolist())
	conn.close
	return 0

def t():
	#df=kk.select('e:/mxk.csv')
	files1='e:/mxk.xlsx'
	#print("读取联赛配置文件，'*.csv'")
	#kk=tooth_excleClass(files1)
	#df=kk.read()
	#print(df[df.xh15==1])
	cp='两球/两球半'
	print(cp)
	print(cp.replace('/','-'))

	files2='yhq_idnm_list.csv'
	idnm=806641
	df_idnm=zqconfigClass(0).select(files2)
	print(df_idnm[df_idnm.idnm==idnm].empty)

	list_files =['利记.csv','Iceland.csv','Bet365.csv']
	print(list_files[0][:-4])
	l=list_files.sort()
	print(list_files)
	print(list_files.index('利记.csv'))

	lll=['10BET', '12BET(壹貳博)', '1Bet', '5Dimes', 'Bet-at-home', 'Bet3000', 'Bet365', 'BetAdria', 'BetClic.fr', 'BetClick', 'BetCRIS', 'Betflag.it', 'Betfred(博发)', 'Betsafe', 'Betshop', 'Betstar', 'Better.it', 'BINGOAL', 'BoDog(博狗)', 'BookieBob', 'Bovada', 'Boylesports', 'Bwin', 'Bwin.es', 'CashPoint', 'Coral', 'Domusbet.it', 'Efbet', 'Eurobet', 'Eurobet.it', 'Expekt', 'Fonbet', 'France-pari.fr', 'Gamebookers', 'Goalbet', 'Gwbet', 'HrvatskaLutrija', 'IBCBET(沙巴)', 'Iceland', 'Iddaa', 'IFortuna.sk', 'Intertops', 'Interwetten', 'Interwetten.es', 'Intralot(因特拉洛)', 'Intralot.it', 'Mansion88(明升)', 'Matchbook', 'MeridianBet', 'Miseojeu', 'MyBet', 'Nike', 'Nordicbet', 'Norway', 'Oddset', 'Olimpkz', 'PaddyPower', 'PartyBets', 'PMU', 'Skybet', 'Smarkets', 'SNAI', 'SportingBet(博天堂)', 'Sportsbet', 'StarPrice', 'STS', 'SuperSport', 'Sweden', 'SynotTIP', 'TheGreek.com', 'Tipico', 'TipKurz', 'Tipsport', 'Titanbet', 'TopSport', 'Tote', 'Totesport', 'Toto', 'TotoSi', 'Unibet.fr', 'Unibet.it', 'Unitab', 'Wewbet(盈禾)', '伟德', '利记', '威廉希尔', '威廉希尔.it', '必发', '易胜博', '澳门', '皇冠', '立博', '香港马会', 'DanskeSpil', 'Fivebet.it', 'Pamestihima', '竞彩官方', '金宝博', '18Bet', 'BetClic.it', 'Betrally', 'BetssonSportsbook', 'Leon', 'NorskTipping', 'SvenskaSpel', 'VBet', 'Milenium', 'Stoiximan', 'Setantabet', 'Unibet(优胜客)', 'Championsbet', 'Isibet', 'Sjbet', 'Tipsport.sk', 'Bookmaker.eu', 'Agile.it', '888Sport', 'Merkur-win', '奥地利博彩', 'Betbright', 'BetfairSB', 'CMD368.com', 'Netbet.fr', 'PlanetWin365', 'BetClic', 'Vernons', 'Winamax.fr', '1xBet', 'GentingBet', 'Stanleybet.it', 'X-TiP', 'Zebet.fr', 'BetfairESSportsbook', 'BetfairUKSportsbook', 'BetVictor', 'Singbet', 'RB88(走地皇)', 'Pinnacle平博', 'iFortuna.cz', 'Marcaapuestas', 'Tipbet', 'Titanbet.es', 'Betano.ro', 'Bethard', 'BetOlimp', 'Betway(必威)', 'Sisal.it', 'CoolBet', 'Giocodigitale.it', 'Babibet', 'Marathon(马博)']
	print(len(lll))		
t()

#z=li_kz2(li1,li1)
#li_kz2(z,li1)
#print(last_sunday_saturday())
#print(last_sunday_saturday())


#print()
#print(list3)
#for x in iter(li):	print(x)