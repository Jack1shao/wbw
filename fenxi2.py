#fenxi2
#
from collections import Counter
from pandas.core.frame import DataFrame
from savedateClass import savedateClass
from zqfenxi import zqfenxi
import numpy as np
from zqconfigClass import zqconfigClass
from zqfenxi_gz import zqfenxi_gz
import os
import pandas as pd

import json
class fenxi2(object):
	"""docstring for fenxi2"""
	def __init__(self, arg):
		super(fenxi2, self).__init__()
		self.arg = arg
		
	def get_bcgs_from_db(self):
		k=savedateClass()
		sql='select DISTINCT o.bcgs from ouzhi o'
		list_d1=k.select(sql)
		list_ii=[]
		[list_ii.append(x[0]) for x in list_d1]
			
		#print(list_ii,len(list_ii))
		return list_ii
	def qingli(self):
		list_ii=self.get_bcgs()
		k=savedateClass()
		iii=0
		list_bcgs=[]
		for x in list_ii:
			iii+=1
			#if iii>2:break
			sql="select count(*) from ouzhi o where o.bcgs='{}'".format(str(x))
			print(sql)
			li=k.select(sql)
			print(x,int(li[0][0]))
			if int(li[0][0])>10000:
				list_bcgs.append(x)
		print(list_bcgs)
		return 0
	def get_bcgs(self):
		list_not_in=['1Bet2Bet.com', '24hBET', '24hPoker', '32RedBet', '888.it', 'Apollobet', 'As3388', 'Bet770', 'Bet7days', 'Betaland', 'BetBoo', 'Betcenter', 'Betchance', 'BetClick.fr', 'Betcruise', 'BetGun.com', 'BetInternet(发达)', 'BetISN(智博)', 'Betliner', 'Betlive', 'BetNGo', 'Betoto', 'Betoto.com', 'Betpeople', 'Betpro.it', 'Betrockit.com', 'Betsafe.DK', 'Betsonic', 'Betsson', 'Betsson.DK', 'BetssonExchang', 'Betting195', 'Betting2000', 'Betway', 'BGT', 'Bookmaker.ag', 'Bwin.fr', 'Bwin.it', 'Canbet', 'CaribSports', 'CBMBookmaker', 'Centurionbet', 'Cirsa', 'Com-bet.com', 'Completesportsbetting', 'DanskTipstjeneste', 'DiamondSportsBook', 'DiamondSportsbookInt.', 'DoxxBet', 'Eccobet', 'Evebet(银河)', 'Evobet', 'Evona', 'E乐博',
					 'Fantasticwin', 'FavBet', 'FlemingtonSportsbet', 'Fubo(富博)', 'Fubo.com', 'GamblersPalace', 'Gamebookers.it', 'Gamenet', 'Giochiamo', 'GLB', 'Globet', 'GoldBet', 'Goldenpark', 'Guts', 'HappyBet', 'Hattrick', 'HeavenBet', 'Hititbet', 'IASbet.com', 'Interwetten.it', 'Iziplay', 'Jaxx', 'Jenningsbet', 'Kajotbet', 'Kogler', 'LinesMaker', 'Marathon', 'MatchPoint', 'Maxi-tip', 'Mermaidbet', 'Millenniumbet', 'Mooregames', 'Mozzart', 'MyBet.com', 'NGG', 'Nikebet', 'Noxwin', 'Offside', 'Offsidebet', 'Optibet', 'OverBet24', 'PaddyPower.it', 'PAF', 'PariMatch', 'Parionsweb', 'Parisport', 'PianetaScommesse', 'Playbet', 'Primebet', 'PublicBet', 'Redbet', 'SAjOO', 'SAjOO.fr', 'Samvo', 'Sazkashop', 'Schwechat', 'Singaporepools', 'Singlebet(SB)', 'Sisal', 'Sportnaloterija', 'Sportplus', 'Sporttip', 'Startip', 'Stravinci', 'SuperSoccer', 'Tabcorp', 'Tattsbet', 'Tempobet', 'TipKurz.sk', 'Tipos', 'Tipp3', 'Tipsport.net', 'Totalbet', 'Totolotek', 'TotoMix', 'Unibet(重复)', 'Victoriatip', 'Vierklee', 'Vietbet', 'VivaroBet', 'VoltBet', 'WagerWeb', 
					 'WBX', 'Wettpunkt', 'WinningGoal', 'Yabet', 'YayBet', 'YouWager', '博天堂.au', '合对', '太阳城', '必发.it', '永利高', 'Adabet', 'BetPhoenix', 'CBMsport', 'FiveBet', 'IslenskarGetraunir', 'Sports-1', 'Sports.com', 'sportsbetting.com.au', 'Sporttery', 'Supermatch', 'Alibet', 'Betsi', 'ABCIslands', 'Jazz', 'Bets4all.com', 'Toals', 'Goalwin', 'Skiller.it', 'MaxOdds', 'OddsRing', 'Etoto', 
					 'Bet-at-home.it', 'Bestbet', 'FortunaWin', 'TheGreek', '利记(香港)', '888皇冠', 'AstraSportBets', 'Egobet', 'Giocodigitale', 'InstantActionSports', 'Inteltek', 'LUXBET', 'Nike.sk', 'Teambet', 'Tipico.it', 'Uwin.com', '平博', '易胜博88(重复)', 'Bookmaker.com', 'Czarnykon', 'Gmatic', 'Oddsen', 'Rebels', 'Remi', 'TopSportWetten', 'Wettbuero', '乐天堂.au', 'ABCmanager', 'Cecebet', 'MDJS', 'Betbutler', 'IACS', 'Bet1128', 'Bet855', 'Betklass.com', 'Sirbobet', 'Cirsa.it', 'Merkur-win.it', 'Riche88(富易堂)', 'Tomwaterhouse', 'Rebatewager', '富易堂', '威廉希尔.es', 'Ball2Win', 'Betcas', 'Betin', '138sungame', '88asia88', 'Balkanbet.rs', 'Betcenter.be', 'BetuniQ', 'BizonBet', 'Contorabet', 'FDJ', 'GameLux.it', 'GSNetwork', 'JoinBet', 'Luckia.es', 'Mobibet', 'Pinnbet', 'SeanieMac', 'SmartLiveSport', 'Starpricebet', 'Vwin', 'Wilsonbet', '申博138', 'Bet16(瑞丰)', 
					 'Gobetgo', 'Mcbookie', 'SuperLenny', '99Bet', 'Bet2be', 'Dashbet', 'Sportium', 'UEDBET(UED亚洲)', 'VictorChandler', '立博.au', '小利', '小永', '18luck(新利)', 'Partypoker', '138.com(重复)', '666Bet', 'BetAdonis', 'Sportsbook.ag', 'Winmasters', 'Bet-at-home.uk', 'BetRoyal', 'CBCX', 'Coliseumbet', 'HollywoodBets', 'RB88', 'Starbet.be', '优德', '申博娱乐', 'Netbet.it', 'Gazzabet', 'Paradisewin', 'SamvoBetBroker', '威廉希尔.au', '12BET', 'Ball365', 'Betcentershops', 'BetfairExchange', 'BetfairITSportsbook', 'Betitaly', 'Leijonakasino', 'Veikkaushuone', 'Vipstakes', 'WinlineBet', '瑞丰国际', '2winbet.gr', 'Betsolo', 'Bitcasino', 'Jojobet', 'Propawin', 'Realdealbet', 'Vitalbet', 'Agile', 'Sportingbet.vu', 'Admiral.at', 'ArtemisBet', '888Sport.es', 'Betmira', 'Betswar', 'ExclusiveBet', 'Otobet', 'Playros', 'Tiplix', 'Betcart', 'Betmonsters', 'Villabet', 'Bet-52', 'Betboro', 'Intragame', 'Leovegas', 'Sekabet', 'Vonbet', 'Wonclub',
					 'ParionsSport', 'READYtoBET', 'VIKS.com', 'LiveTest', 'BetEast', 'Betballer', 'Betncatch', 'Casinosahara', 'Marsbetting', 'MrRingo', '777.dk', 'Iforbet.pl', 'Paris365', 'Spreadex', 'LSbet', 'Bet365Mobile', 'Livebet', '108bet', 'Royrichie', 'Betregal', 'Interbet', '英国约翰G']
		list_in=['10BET', '12BET(壹貳博)', '1Bet', '5Dimes', 'Bet-at-home', 'Bet3000', 'Bet365', 
				'BetAdria', 'BetClic.fr', 'BetClick', 'BetCRIS', 'Betflag.it', 'Betfred(博发)', 'Betsafe', 
				'Betshop', 'Betstar', 'Better.it', 'BINGOAL', 'BoDog(博狗)', 'BookieBob', 'Bovada', 'Boylesports', 
				'Bwin', 'Bwin.es', 'CashPoint', 'Coral', 'Domusbet.it', 'Efbet', 'Eurobet', 'Eurobet.it', 'Expekt',
				'Fonbet', 'France-pari.fr', 'Gamebookers', 'Goalbet', 'Gwbet', 'HrvatskaLutrija', 'IBCBET(沙巴)', 'Iceland', 'Iddaa', 'IFortuna.sk', 'Intertops', 'Interwetten', 'Interwetten.es', 'Intralot(因特拉洛)', 'Intralot.it', 'Mansion88(明升)', 'Matchbook', 'MeridianBet', 'Miseojeu', 'MyBet', 'Nike', 'Nordicbet', 'Norway', 'Oddset', 'Olimpkz', 'PaddyPower', 'PartyBets', 'PMU', 'Skybet', 'Smarkets', 'SNAI', 'SportingBet(博天堂)', 'Sportsbet', 'StarPrice', 'STS', 'SuperSport', 'Sweden', 'SynotTIP', 'TheGreek.com', 'Tipico', 'TipKurz', 'Tipsport', 'Titanbet', 'TopSport', 'Tote', 'Totesport', 'Toto', 'TotoSi', 'Unibet.fr', 'Unibet.it', 'Unitab', 'Wewbet(盈禾)', '伟德', '利记', '威廉希尔', '威廉希尔.it', '必发', '易胜博', '澳门',
				'皇冠', '立博', '香港马会', 'DanskeSpil', 'Fivebet.it', 'Pamestihima', '竞彩官方', '金宝博', '18Bet', 'BetClic.it', 'Betrally', 'BetssonSportsbook', 'Leon', 'NorskTipping', 'SvenskaSpel', 'VBet', 'Milenium', 'Stoiximan', 'Setantabet', 'Unibet(优胜客)', 'Championsbet', 'Isibet', 'Sjbet', 'Tipsport.sk', 'Bookmaker.eu', 'Agile.it', '888Sport', 'Merkur-win', '奥地利博彩', 'Betbright', 'BetfairSB', 'CMD368.com', 'Netbet.fr', 'PlanetWin365', 'BetClic', 'Vernons', 'Winamax.fr', '1xBet', 'GentingBet', 'Stanleybet.it', 'X-TiP', 'Zebet.fr', 'BetfairESSportsbook', 'BetfairUKSportsbook', 'BetVictor', 'Singbet', 'RB88(走地皇)', 'Pinnacle平博', 'iFortuna.cz', 'Marcaapuestas', 'Tipbet', 'Titanbet.es', 'Betano.ro', 'Bethard', 'BetOlimp', 'Betway(必威)', 'Sisal.it', 'CoolBet',
				'Giocodigitale.it', 'Babibet', 'Marathon(马博)']
		li=self.get_bcgs_from_db()

		list_yy=[]
		for x in li:
			if x in list_not_in:continue
			if x in list_in:
				list_yy.append(x)
		print(list_yy,len(list_yy))

		return list_yy

	def get_bssj_from_db(self,bcgs):
		#bcgs='Sweden'
		sql="SELECT DISTINCT s.idnm,s.ls,s.nd,s.zd,s.kd,s.zjq,s.kjq,y.jp,y.cp,o.bcgs,o.chf,o.jhf,o.ck3,o.ck1,o.ck0,o.jk3,o.jk1,o.jk0,o.cz3,o.cz1,o.cz0,"
		sql+="(SELECT DISTINCT b.gl-b.bf from 	bifa b WHERE b.idnm=s.idnm and b.xh=1 ) as glc3,"
		sql+="(SELECT DISTINCT b.gl-b.bf from 	bifa b WHERE b.idnm=s.idnm and b.xh=2 ) as glc1,"
		sql+=" (SELECT DISTINCT b.gl-b.bf from 	bifa b WHERE b.idnm=s.idnm and b.xh=3 ) as glc0,"
		sql+="(SELECT DISTINCT b.ykzs from 	bifa b WHERE b.idnm=s.idnm and b.xh=1 ) as ykzs3,"
		sql+="(SELECT DISTINCT b.ykzs from 	bifa b WHERE b.idnm=s.idnm and b.xh=2 ) as ykzs1,"
		sql+="(SELECT DISTINCT b.ykzs from 	bifa b WHERE b.idnm=s.idnm and b.xh=3 ) as ykzs0,"
		sql+="(select DISTINCT bs.s1 from sjtdbf bs where bs.idnm=s.idnm) as bss1,"
		sql+="(select DISTINCT bs.s2 from sjtdbf bs where bs.idnm=s.idnm) as bss2,"
		sql+="(select DISTINCT bs.s3 from sjtdbf bs where bs.idnm=s.idnm) as bss3"

		sql+=" FROM scb s,yapan y,bifa bf,ouzhi o "
		sql+=" where 1=1	and o.idnm=s.idnm	and bf.idnm=s.idnm	and y.idnm=s.idnm	and y.ypgs='Bet365'"
		sql+=" and o.bcgs in ('{}')".format(bcgs)
		print(sql)
		k=savedateClass()
		li=k.select(sql)
		#print(li)
		columns=['idnm','ls','nd','zd','kd','zjq','kjq','jp','cp','bcgs','chf','jhf','ck3','ck1','ck0','jk3','jk1','jk0','cz3','cz1','cz0','glc3','glc1','glc0','ykzs3','ykzs1','ykzs0','bss1','bss2','bss3']
		df=DataFrame(list(li),columns=columns)
		#print(df.head())
		
		return df
	def get_bssj_from_csv(self):
		kk=zqconfigClass(0)
		df=kk.select('e:/555.csv')
		#print(df.head())
		return df
	#计算离散度
	def jslsd(self,list_sg):
		kk=zqfenxi_gz()
		list_r=[]
		cc=kk.count(list_sg)
		lll=cc.values[0]
		li=[]
		li.append(lll[0]+lll[1])
		li.append(lll[2])
		li.append(lll[3])
		lsxi,fc=kk.lisan(li)
		list_r.extend(lll)
		list_r.append('-')
		list_r.extend(li)
		list_r.append(lsxi)
		list_r.append(fc)
		return list_r
	#从数据库中获取各欧赔公司的数据，to_csv get_ouzhi_to_csv import fenxi2 
	def get_ouzhi_to_csv(self):
		#从数据库中获取各欧赔公司的数据，to_csv
		list_bcgs=self.get_bcgs()
		print(list_bcgs)
		for bcgs in list_bcgs:
			files='e:/football/csv/{}.csv'.format(bcgs)
			print(files)
			df=self.get_bssj_from_db(bcgs)
			#print(df.head())
			df.to_csv(files,encoding="utf_8_sig")
			
		return 0	
	

	def test(self):
		
		df=self.get_bssj_from_csv()
		df=df[df.n58=='半球']
		list_mx=[31,32,11,12,101,102]
		list_yp=['球半', '半球', '两球', '一球', '受一球/球半', '一球', '平手/半球', '平手', '受半球/一球', '受球半', '受平手/半球', '受半球', '半球/一球', '受一球', '两球/两球半', '受两球', '球半/两球', '两球半', '受两球/两球半', '一球/球半', '三球/三球半', '三球', '受球半/两球', '两球半/三球', '受两球半', '三球半', '受两球半/三球']

		for x in list_mx:
			sss='n9:{}'.format(x)
			df1=df[(df.n9==x)]
			list_lsd=self.jslsd( list(df1.n2.values))
			list_lsd.insert(0,sss)
			print(list_lsd)
			sss='n16:{}'.format(x)
			df1=df[(df.n30==x)]
			list_lsd=self.jslsd( list(df1.n2.values))
			list_lsd.insert(0,sss)
			print(list_lsd)


		for x in list_mx:
			sss='Bet365模型:{}'.format(x)
			for y in list_mx:
				sss1=' will模型:{}'.format(y)
				df1=df[(df.n9==x)&(df.n37==y)]
				list_lsd=self.jslsd( list(df1.n2.values))
				list_lsd.insert(0,sss+sss1)
				print(list_lsd)
		return 0
	def test2(self):
		list_mx=[31,32,11,12,101,102]
		list_yp=['球半', '半球', '两球', '一球', '受一球/球半', '一球', '平手/半球', '平手', '受半球/一球', '受球半', '受平手/半球', '受半球', '半球/一球', '受一球', '两球/两球半', '受两球', '球半/两球', '两球半', '受两球/两球半', '一球/球半', '三球/三球半', '三球', '受球半/两球', '两球半/三球', '受两球半', '三球半', '受两球半/三球']

		path_f='e:/football/csv/'
		uu=zqfenxi_gz()
		kk=zqconfigClass(0)
		list_files=os.listdir(path_f)
		for files in list_files:
			print(path_f+files)
			df=kk.select(path_f+files)
			#生成模型
			df_mx=uu.get_mx(df)

			for yp in list_yp:
				list_to_csv=[]
				df=df_mx[df_mx.cp==yp]

				for x in list_mx:

					sss='{}'.format(x)
					df1=df[df.c_klmx==x]
					if df1.empty:
						print('kong')
						continue
					list_lsd=self.jslsd( list(df1.sg.values))
					list_lsd.insert(0,sss)
					list_lsd.append(yp)
					list_lsd.append(files)
					list_to_csv.append(list_lsd)
					print(list_lsd)
				df=DataFrame(list_to_csv)
				df.to_csv('e:/football/mxk.csv',mode='a',header=False,encoding="utf_8_sig")
		return 0
	def test3(self):
		list_files =['威廉希尔.csv','Iceland.csv','Bet365.csv']
		list_files.sort()
		path_f='e:/football/csv/'
		uu=zqfenxi_gz()
		kk=zqconfigClass(0)

		#生成模型

		df=kk.select(path_f+'Bet365.csv')
		df=df[df.cp=='一球']
		df_mx3=uu.get_mx(df)
		print(df_mx3.head())
		print(len(df_mx3))

		for files in list_files:
			if files=='Bet365.csv':continue
			print(files)
			df=kk.select(path_f+files)
			df=df[df.cp=='一球']

			df_mx2=uu.get_mx(df)[['idnm','bcgs','c_klmx','c_zz','c_fh','j_klmx']]
			print(df_mx2.head())
			df_mx3=pd.merge(df_mx3,df_mx2,how='left',on='idnm')

		#df=pd.merge(df_lj,df_mx,how='left',on='idnm')
		#print(df_lj.columns.values)
		#print(len(df_lj))
		#print(df_lj[['idnm','cp_x']])
		df_mx3.to_csv('e:/football/mx33.csv',encoding="utf_8_sig")

#uu=fenxi2(0)
#uu.qingli()
#uu.lisan([3766,3302,2955,2821])
#uu.count('')
#uu.get_bssj_from_csv()