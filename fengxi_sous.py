#zqconfigClass.py

from zqconfigClass import zqconfigClass
from tooth_excle import tooth_excleClass
from zqfenxi_gz import zqfenxi_gz



files='e:/football/半球1213.xlsx'
hh=tooth_excleClass(files)
df=hh.read()
#print(dr)
tt=[['Bet365',11],['Iceland',102]]
b,df_1=saixuan(df,tt)
print(b)
print(df_1)
print(count_sg(df_1))
'''	if cc!='':
		dr2=dr[dr[cc].isin(jlist)]
		sg_list=list(dr2.sg.values)
		print(sg_list)
		kk=zqfenxi_gz().count(sg_list)
		print(kk)'''

	