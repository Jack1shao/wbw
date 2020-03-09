#MACD

#初始化变量
收盘价列表 = []     #新建收盘价列表
diff列表 = []      #新建diff列表
dea列表 = []       #新建dea列表
短周期 = 12        #用于计算短期指数移动平均的周期
长周期 = 26        #用于计算长期指数移动平均的周期
dea周期 = 9        #用于计算dea指数移动平均的周期

#获取数据
for i in range(0, total):
    收盘价 = get("收盘价", i)     #获取收盘价
    收盘价列表.append(收盘价)     #将收盘价储存在"收盘价列表"中, 用于后续计算

#计算数据并储存用于画线的数据
for i in range(0, total):
    短期指数移动平均 = EMA(收盘价列表, 短周期, i)   #计算短期指数移动平均
    长期指数移动平均 = EMA(收盘价列表, 长周期, i)   #计算长期指数移动平均
    diff = 短期指数移动平均 - 长期指数移动平均      #计算diff值
    diff列表.append(diff)                       #将diff值存在diff列表中
    dea = EMA(diff列表, dea周期, i)              #计算dea值
    dea列表.append(dea)                         #将dea值保存到dea列表中
    macd = 2 * (diff - dea)                     #计算macd值
    save("DIFF", diff, i)                       #将diff值储存在"DIFF"对象中并用于画线
    save("DEA", dea, i)                         #将dea值储存在"DEA"对象中并用于画线
    save("MACD", macd, i)                       #将macd值储存在"MACD"对象中并用于画线

#画出储存好数据的线
draw.curve("DIFF", 15)            #画出"DIFF"折线
draw.curve("DEA", 7)              #画出"DEA"折线
draw.color_stick("MACD")          #画出"MACD"红涨绿跌图