# Python 股票历史数据的获取
# 标签： pythonA股数据K线多线程


# 获取股票数据的接口很多，免费的接口有新浪、网易、雅虎的API接口，收费的就是证券公司及相应的公司提供的接口。
# 收费试用的接口一般提供的数据只是最近一年或三年的，限制比较多，除非money足够多。
# 所以本文主要讨论的是免费数据的获取及处理。

# 国内提供股票数据的接口如sinajs，money.163.com，yahoo，它们提供的API接口不同，每家提供的数据大同小异，可以选择一家的数据来处理。
# 目前，国内有一个开源的财经数据获取包，封装了上述的接口，不需关系数据源从哪去，它会优先从最快的源来取数据。使用起来非常方便。它是TuShare，具体的安装使用见链接。

# 本文基于TuShare的数据获取基础上开发，介绍如何获取A股所有股票的历史K线数据。

# 一、获取A股上市公司列表

import tushare as ts
import pandas as pd
def download_stock_basic_info():

    try:
        df = ts.get_stock_basics()
        #直接保存到csv
        print('choose csv')
        df.to_csv('stock_basic_list.csv');
        print('download csv finish')

# 股票列表中包括当前A股的2756只股票的基本信息，包括：

# code,代码
# name,名称
# industry,所属行业
# area,地区
# pe,市盈率
# outstanding,流通股本
# totals,总股本(万)
# totalAssets,总资产(万)
# liquidAssets,流动资产
# fixedAssets,固定资产
# reserved,公积金
# reservedPerShare,每股公积金
# eps,每股收益
# bvps,每股净资
# pb,市净率
# timeToMarket,上市日期

# 二、获取单只股票的历史K线

# 获取的日K线数据包括：

# date : 交易日期 (index)
# open : 开盘价（前复权，默认）
# high : 最高价（前复权，默认）
# close : 收盘价（前复权，默认）
# low : 最低价（前复权，默认）
# open_nfq : 开盘价（不复权）
# high_nfq : 最高价（不复权）
# close_nfq : 收盘价（不复权）
# low_nfq : 最低价（不复权）
# open_hfq : 开盘价（后复权）
# high_hfq : 最高价（后复权）
# close_hfq : 收盘价（后复权）
# low_hfq : 最低价（后复权）
# volume : 成交量
# amount : 成交金额

# 下载股票代码为code的股票历史K线，默认为上市日期到今天的K线数据，支持递增下载，如本地已下载股票60000的数据到2015-6-19，再次运行则会从6.20开始下载，追加到本地csv文件中。

# 默认为上市日期到今天的K线数据
# 可指定开始、结束日期：格式为"2015-06-28"
def download_stock_kline(code, date_start='', date_end=datetime.date.today()):

    code = util.getSixDigitalStockCode(code) # 将股票代码格式化为6位数字

    try:
        fileName = 'h_kline_' + str(code) + '.csv'

        writeMode = 'w'
        if os.path.exists(cm.DownloadDir+fileName):
            #print (">>exist:" + code)
            df = pd.DataFrame.from_csv(path=cm.DownloadDir+fileName)

            se = df.head(1).index #取已有文件的最近日期
            dateNew = se[0] + datetime.timedelta(1)
            date_start = dateNew.strftime("%Y-%m-%d")
            #print date_start
            writeMode = 'a'

        if date_start == '':
            se = get_stock_info(code)
            date_start = se['timeToMarket']
            date = datetime.datetime.strptime(str(date_start), "%Y%m%d")
            date_start = date.strftime('%Y-%m-%d')
        date_end = date_end.strftime('%Y-%m-%d')

        # 已经是最新的数据
        if date_start >= date_end:
            df = pd.read_csv(cm.DownloadDir+fileName)
            return df

        print 'download ' + str(code) + ' k-line >>>begin (', date_start+u' 到 '+date_end+')'
        df_qfq = ts.get_h_data(str(code), start=date_start, end=date_end) # 前复权
        df_nfq = ts.get_h_data(str(code), start=date_start, end=date_end) # 不复权
        df_hfq = ts.get_h_data(str(code), start=date_start, end=date_end) # 后复权

        if df_qfq is None or df_nfq is None or df_hfq is None:
            return None

        df_qfq['open_no_fq'] = df_nfq['open']
        df_qfq['high_no_fq'] = df_nfq['high']
        df_qfq['close_no_fq'] = df_nfq['close']
        df_qfq['low_no_fq'] = df_nfq['low']
        df_qfq['open_hfq']=df_hfq['open']
        df_qfq['high_hfq']=df_hfq['high']
        df_qfq['close_hfq']=df_hfq['close']
        df_qfq['low_hfq']=df_hfq['low']

        if writeMode == 'w':
            df_qfq.to_csv(cm.DownloadDir+fileName)
        else:

            df_old = pd.DataFrame.from_csv(cm.DownloadDir + fileName)

            # 按日期由远及近
            df_old = df_old.reindex(df_old.index[::-1])
            df_qfq = df_qfq.reindex(df_qfq.index[::-1])

            df_new = df_old.append(df_qfq)
            #print df_new

            # 按日期由近及远
            df_new = df_new.reindex(df_new.index[::-1])
            df_new.to_csv(cm.DownloadDir+fileName)
            #df_qfq = df_new

        print '\ndownload ' + str(code) +  ' k-line finish'
        return pd.read_csv(cm.DownloadDir+fileName)

    except Exception as e:
        print str(e)


    return None

##  private methods  ##
#######################

# 获取个股的基本信息：股票名称，行业，地域，PE等，详细如下
#     code,代码
#     name,名称
#     industry,所属行业
#     area,地区
#     pe,市盈率
#     outstanding,流通股本
#     totals,总股本(万)
#     totalAssets,总资产(万)
#     liquidAssets,流动资产
#     fixedAssets,固定资产
#     reserved,公积金
#     reservedPerShare,每股公积金
#     eps,每股收益
#     bvps,每股净资
#     pb,市净率
#     timeToMarket,上市日期
# 返回值类型：Series
def get_stock_info(code):
    try:
        sql = "select * from %s where code='%s'" % (STOCK_BASIC_TABLE, code)
        df = pd.read_sql_query(sql, engine)
        se = df.ix[0]
    except Exception as e:
        print str(e)
    return se

# 三、获取所有股票的历史K线

# 获取所有股票的历史K线
def download_all_stock_history_k_line():
    print 'download all stock k-line'
    try:
        df = pd.DataFrame.from_csv(cm.DownloadDir + cm.TABLE_STOCKS_BASIC + '.csv')
        pool = ThreadPool(processes=10)
        pool.map(download_stock_kline, df.index)
        pool.close()
        pool.join()

    except Exception as e:
        print str(e)
    print 'download all stock k-line'

# Map来自函数语言Lisp，map函数能够按序映射出另一个函数。

# urls = ['http://www.yahoo.com', 'http://www.reddit.com']
# results = map(urllib2.urlopen, urls)

# Map原理

# 有两个能够支持通过map函数来完成并行的库：一个是multiprocessing，另一个是鲜为人知但功能强大的子文件：multiprocessing.dummy。
# Dummy就是多进程模块的克隆文件。唯一不同的是，多进程模块使用的是进程，而dummy则使用线程（当然，它有所有Python常见的限制）。

# 通过指定processes的个数来调用多线程。

# 附：文中用到的其他函数及变量，定义如下：

# TABLE_STOCKS_BASIC = 'stock_basic_list'
# DownloadDir = os.path.pardir + '/stockdata/' # os.path.pardir: 上级目录

# 补全股票代码(6位股票代码)
# input: int or string
# output: string
def getSixDigitalStockCode(code):
    strZero = ''
    for i in range(len(str(code)), 6):
        strZero += '0'
    return strZero + str(code)
