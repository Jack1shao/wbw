#zqfenxi.py
from tooth_excle import tooth_excleClass
class zqfenxi(object):
	"""docstring for zqfenxi"""
	def __init__(self, arg):
		super(zqfenxi, self).__init__()
		self.arg = arg
		self.idnm=int(arg)

	def iceland(self):
		df=tooth_excleClass('e:/0.5.xlsx').read()
		#按列值分组
		df1=df[df.bcgs=='Iceland']
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
