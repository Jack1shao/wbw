#新手用户可以直接在基础样例模板空白处填写代码, 老用户请Ctrl+A删除模板

#变量初始化区域
收盘价列表=[]
开盘价列表=[]
昨收价列表=[]
最高价列表=[]
最低价列表=[]
交易量列表=[]
#涨幅列表=[]
cci=[]
c1=[]
c2=[]
N=14
#取数据区域
for i in range(0, total):
    #pass  #请忽略这行代码, 它并不影响你写的其他代码
    收盘价=get("收盘价", i)
    开盘价=get("开盘价", i)
    昨收价=get("昨收价", i)
    最高价=get("最高价",i)
    最低价=get("最低价",i)
    交易量=get("交易量",i)
    收盘价列表.append(收盘价)
    昨收价列表.append(昨收价)
    开盘价列表.append(开盘价)
    最高价列表.append(最高价)
    最低价列表.append(最低价)
    交易量列表.append(交易量)
    
    c1.append(130)
    c2.append(-80)
ma1=[]
md1=[]
typ1=[]
std1=[]
std2=[]
#计算数据区域
for i in range(0, total):
    #pass  #请忽略这行代码, 它并不影响你写的其他代码
    #涨幅=(收盘价列表[i]-昨收价列表[i])/昨收价列表[i]
    #save("DIFF", diff, i)
    typ=(最高价列表[i]+最低价列表[i]+收盘价列表[i])/3
    typ1.append(typ)
for i in range(0, total):
    a=MA(typ1,N,i)
    ma1.append(a)
for i in range(0, total):
    d=abs(ma1[i]-typ1[i])
    std=STD(typ1,N,i)
    std1.append(std)
    md1.append(d)

    #save("收盘价", 收盘价列表[i], i)
#计算数据区域
for i in range(0, total):
    d=STD(md1,N,i)
    std2.append(d)
    #save("收盘价", 收盘价列表[i], i)
#CCI（N日）=（TP－MA）÷MD÷0.015
for i in range(0, total):
    #CCI:(TYP-MA(TYP,N))/(0.015*AVEDEV(TYP,N));
    cci=(typ1[i]-ma1[i])/(std1[i]*0.015)
    save("cci1", cci, i)
    save("typ1", typ1[i], i)
    save("c2", c2[i], i)
    save("c1", c1[i], i)



#画线区域
#draw.curve("typ1")
#draw.curve("c2")
#draw.curve("c1")
draw.curve("cci1")
#set.coordinate_axis("涨幅", "%")
