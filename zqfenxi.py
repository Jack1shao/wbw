#zqfenxi.py
from tooth_excle import tooth_excleClass
class zqfenxi(object):
	"""docstring for zqfenxi"""
	def __init__(self, arg):
		super(zqfenxi, self).__init__()
		self.arg = arg
		self.idnm=int(arg)

	def _ice(self,df,idnm):

		df1=df[(df.idnm==779598)&(df.bcgs=='Iceland')]
		#print(df1.zjq,df1.kjq)
		list2=[]
		for index,x in df1.iterrows():
			#print(x.zjq-x.kjq)
			sg=x.zjq-x.kjq
			if sg==0:list2.append("平")
			elif sg<0:list2.append("负")
			elif sg==1:
				list2.append('胜一球')
			else :list2.append('胜')

			#亚盘变化
			

			#赔付
			if x.ck1>x.ck3 or x.ck0>x.ck3:
				list2.append('赔付不正常')
			else:
				list2.append('赔付正常')

			#返还率变化
			if x.chf-x.jhf>0:
				list2.append('返还率-降')
			elif x.chf-x.jhf==0:
				list2.append('返还率未变')
			else：
				list2.append('返还率-升')

			#平局盈亏情况

			if x.ykzs1>=20 and x.ykzs<=30:
				list2.append('平局过冷')
			elif x.ykzs1>30
				list2.append('平局大冷')
			elif x.ykzs1>0 and x.ykzs1<20
				list2.append('平局过热')
			else:
				list2.append('平局热-{}'.format(x.ykzs1))	





		return df1
	def iceland(self):
		df=tooth_excleClass('e:/0.5.xlsx').read()
		#按列值分组
		#df1=df[df.bcgs=='Iceland']
		#df1=df1[df1.idnm==779599]
		df1=self._ice(df,779598)
		print(len(df1))
		print(df1.head())
		#赛果
		
		#赔率情况
		#赔付情况
		#返还率情况
		#盈亏指数
		#必发概率情况
		#亚盘初盘情况
		#交叉盘情况
		return 0
h=zqfenxi('1').iceland()
