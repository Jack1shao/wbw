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
	def dr_cci2(self,code,ktype):
		kk=gu_save('')
		hh=gu_zb(0)
		#取4个类型的df
		df=kk.get_k_from_api(code,ktype)
		#取4个类型的CCi
		if df.empty:
			return 0
		cci=hh.cci(df)[-self.total:]
		#4个类型的顶点
		#画出最后3条线
		fig, ax = plt.subplots(2, 1, figsize=(16,8))
		ax[0].set_title(code+'--'+ktype)
		ax[1].plot(cci,'r')
		#取顶点
		up_li2,line_li=hh.draw_dd_up(cci)
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
		
		df=df[-self.total:]
		mpf.candlestick2_ochl(ax=ax[0],opens=df["open"].values.tolist(), closes=df["close"].values, highs=df["high"].values, lows=df["low"].values,width=0.7,colorup='r',colordown='g',alpha=0.7)
		
		ax[1].axhline(y=100, color='b', linestyle=':')
		ax[1].axhline(y=-100, color='b', linestyle=':')
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
			bz=g.dr_cci2('600598',k)
			if bz==0:
				print('该代码无数据')
				break

if __name__ == '__main__':
	main()
