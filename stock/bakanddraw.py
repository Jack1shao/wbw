from operClass import file_op
import tushare as ts
import datetime

import math
from gu_zb import gu_zb
import talib
import matplotlib.pyplot as plt
import mpl_finance as mpf
import numpy as np
from stockmd import jiekou

def bakanddraw(code,typ,start,end,path):
	'''取重要数据备份并保存图片'''
	kk=jiekou()
	op=file_op()
	
	ktype=typ
	df=kk.getkl(code,ktype)
	if end>start and end<len(df):
		df=df[start:end]
	
	dat11=df.iloc[-1:].date.values[0].split()[0]
	#保存路径和文件
	file1='{0}-{1}-bak-{2}.csv'.format(code,ktype,dat11)
	df.to_csv(file1)
	print(file1)

	hh=gu_zb(0)
	name=''

	#取4个类型的CCi
	if df.empty:
		return 0
	cci=hh.cci(df)
	ln=len(cci)
	
	total=ln-14
	if ln<total:
		total=ln
	PLUS_DI,MINUS_DI,ADX,ADXR=hh.dmi(df)
	df=df[-total:]
	cci=cci[-total:]
	MINUS_DI=MINUS_DI[-total:]
	PLUS_DI=PLUS_DI[-total:]
	ADX=ADX[-total:]
	ADXR=ADXR[-total:]
	
	#4个类型的顶点
	#画出最后3条线

	fig, ax = plt.subplots(3, 1, figsize=(16,8))
	ax[0].set_title(name+code+'--'+ktype,fontproperties = 'SimHei',fontsize = 20)
	ax[1].plot(cci,'r')
	ax[2].plot(ADX,'r')
	ax[2].plot(PLUS_DI,'y')
	ax[2].plot(MINUS_DI,'b')
	ax[2].plot(ADXR,'g')
	ax[2].axhline(y=80, color='b', linestyle=':')
	ax[2].axhline(y=50, color='b', linestyle=':')
	ax[2].axhline(y=20, color='b', linestyle=':')
	#取顶点
	up_li2=hh.gjbc(df)
	dw_li2=hh.gj_d_bl(df)

	print(up_li2)
	if len(up_li2)>4:
		up=up_li2[-4:]
	else:
		up=up_li2

	if len(dw_li2)>2:
		dw=dw_li2[-2:]
	else:
		dw=dw_li2

	for u in up:
		y1=u[1]
		y2=u[3]
		x1=u[0]
		x2=u[2]
		k=(y2-y1)/(x2-x1)
		if k>0:continue
		b=y2-k*x2
		c1=(300-b)/k
		c2=(-200-b)/k
		if c2>total:
			c2=total
		if c1<0:
			c1=0
		l_x=np.linspace(c1,c2,10)
		y=k*l_x+b
		ax[1].plot(l_x,y,'-.y')
	for u in dw:
		y1=u[1]
		y2=u[3]
		x1=u[0]
		x2=u[2]
		k=(y2-y1)/(x2-x1)
		if k<0:continue
		b=y2-k*x2
		c1=(200-b)/k
		c2=(-350-b)/k
		if c1>total:
			c1=total
		if c2<0:
			c2=0
		l_x=np.linspace(c1,c2,10)
		y=k*l_x+b
		ax[1].plot(l_x,y,'-.y')
	#画K线
	mpf.candlestick2_ochl(ax=ax[0],opens=df["open"].values.tolist(), closes=df["close"].values, highs=df["high"].values, lows=df["low"].values,width=0.7,colorup='r',colordown='g',alpha=0.7)
	ax[1].axhline(y=100, color='b', linestyle=':')
	ax[1].axhline(y=-100, color='b', linestyle=':')
	#文字
	plt.style.use('ggplot')
	plt.show()
	return 1

bakanddraw('002498','30',357,468,'')