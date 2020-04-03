#gu_draw.py
from gu_zb import gu_zb
from gu_save import gu_save

import talib
import matplotlib.pyplot as plt
import mpl_finance as mpf
import numpy as np
class gu_draw(object):
	"""docstring for gu_draw"""
	def __init__(self, arg):
		super(gu_draw, self).__init__()
		self.arg = arg
		self.total=120
		#大顶：背驰线之上，股价创新高，cci下折
	def jddd(self,df):
		high_li=df.high.values.tolist()
		close_li=df.close.values.tolist()
		open_li=df.open.values.tolist()
		kk=gu_zb('')
		cci=kk.cci(df)
		ln=len(cci)
		jddd_li=[]
		for i in range(2,ln):
			cn1=high_li[i-2]<high_li[i-1] and high_li[i-1]<high_li[i]
			cn2=close_li[i]>close_li[i-1] and close_li[i-1]>close_li[i-2]
			cn3=close_li[i]>open_li[i] and close_li[i-1]>open_li[i-1] and close_li[i-2]>open_li[i-2]
			cn4=cci[i]<cci[i-1]
			if cn1 and cn2 and cn3 and cn4:
				jddd_li.append([i,'d'])
		open_li.clear()
		close_li.clear()
		high_li.clear()
		return jddd_li
	#无效k线
	def wxkx(self,df):
		high_li=df.high.values.tolist()
		low_li=df.low.values.tolist()
		wx_li=[]
		ln=len(high_li)
		for i in range(0,ln):
			cn1=high_li[i]<=high_li[i-1]
			cn2=low_li[i]<=low_li[i-1]
			if cn1 and cn2:
				wx_li.append(i)
		return wx_li

	
	#到拐点的距离
	def gdjl(self,df):
		kk=gu_zb('')
		cci=kk.cci(df)
		up_li,dw_li=kk.cci_ana_dd(cci)
		wx_li=self.wxkx(df)
		ln=len(cci)
		gd_li=[]
		gd_li.append([0,0])
		wx=0
		for i in range(1,ln):
			if i in wx_li:wx+=1
			if i in up_li or i in dw_li:
				s=i-gd_li[-1][0]-wx+1
				wx=0
				gd_li.append([i,s])

		s=ln-gd_li[-1][0]
		gd_li.append([ln,s])
		return gd_li

	def dr_cci2(self,code,ktype):
		kk=gu_save('')
		hh=gu_zb(0)
		#取4个类型的df
		df=kk.get_k_from_api(code,ktype)
		#取4个类型的CCi
		if df.empty:
			return 0
		cci=hh.cci(df)[-self.total:]
		df=df[-self.total:]
		#df=df[-self.total:]
		#4个类型的顶点
		#画出最后3条线
		fig, ax = plt.subplots(2, 1, figsize=(16,8))
		ax[0].set_title(code+'--'+ktype)
		ax[1].plot(cci,'r')
		#取顶点
		up_li2,line_li=hh.gjbc(df)
		print(up_li2)
		if len(up_li2)>3:
			up=up_li2[-3:]
		else:
			up=up_li2
		for u in up_li2:
			y1=u[1]
			y2=u[3]
			x1=u[0]
			x2=u[2]
			k=(y2-y1)/(x2-x1)
			if k>0:continue
			b=y2-k*x2
			c1=(300-b)/k
			c2=(-200-b)/k
			if c2>self.total:
				c2=self.total
			if c1<0:
				c1=0
			l_x=np.linspace(c1,c2,10)
			y=k*l_x+b
			ax[1].plot(l_x,y,'-.y')

		#画K线
		
		
		mpf.candlestick2_ochl(ax=ax[0],opens=df["open"].values.tolist(), closes=df["close"].values, highs=df["high"].values, lows=df["low"].values,width=0.7,colorup='r',colordown='g',alpha=0.7)
		
		ax[1].axhline(y=100, color='b', linestyle=':')
		ax[1].axhline(y=-100, color='b', linestyle=':')
		#文字
		gd_li=self.gdjl(df)
		jddd_li=self.jddd(df)
		for x in gd_li:
			plt.text(x[0],0,x[1],size = 10)
		for x in jddd_li:
			plt.text(x[0],250,x[1],size = 12)

		plt.show()
		return 1

def main():
	print('this message is from main function')
	g=gu_draw('')
	i=0
	ktype=['30','D','w','m']
	while i<10:
		i+=1
		print('请输入股票代码：           --退出<99>')
		print('99--退出<99>')
	
		cc=input()
		if cc=='99':
			print('	退出<99>')
			break
		code=str(cc)
		if len(code)!=6:
			print('代码错误')
			continue
		for  k in ktype:
			bz=g.dr_cci2(code,k)
			if bz==0:
				print('该代码无数据')
				break

if __name__ == '__main__':
	main()
