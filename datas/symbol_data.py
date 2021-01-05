# -*- coding:utf-8 -*-
import os
path=os.path.abspath('.') 
import pandas as pd
import datetime as dt
import pandas_datareader as pdr
from datas import stock_info, date, analysis, sql_data
import numpy as np
import yfinance as yf
from config.config import *

sp500_dict = {
    'Communication Services': 'COM 通讯服务',
    'Consumer Discretionary': 'CND 可选消费品',
    'Consumer Staples': 'CNS 消费品',
    'Energy': 'ENE 能源',
    'Financials': 'FIN 金融',
    'Health Care': 'HLT 医疗健康',
    'Industrials': 'IND 工业',
    'Materials': 'MAT 材料',
    'Real Estate': 'REI 房地产',
    'Information Technology': 'TEC 信息技术',
    'Utilities': 'UTL 公用事业',
}


def download(code, start, end, source='yahoo'):
    yf.pdr_override()
    if code == '^SPX' :
        source = 'stooq'
        data = pdr.DataReader(code,source, start=start, end=end)
        print(data)
    if source == 'yahoo':
        try:
            data = pdr.DataReader(code, source, start=start, end=end)
        except:
            data = pdr.get_data_yahoo(code, start=start, end=end)
    if source == 'fred':
        data = pdr.DataReader(code, source, start=start, end=end)
    return data


def updateFinanceToDB():
    # dict_db = '{}/datas/db/{}.db'.format(path, config.get('database', 'data_dict'))
    finance_db = '{}/datas/db/{}.db'.format(path,config.get('database', 'finance'))
    # dict_data = sql_data.readDB(dict_db, config.get('tablename', 'data_dict'))
    dict_data = pd.read_csv(path + "/config/financial_data_dict.csv")
    finance_list = dict_data["Symbol"].tolist()
    start = date.get_10year_ago()
    end = date.get_current_day()
    yesterday = dt.datetime.strptime(date.get_yesterday() , '%Y-%m-%d')
    last_trad_day = date.get_current_day()
    vti = download('VTI', start=start, end=end)
    vti = vti.reset_index()
    vti.rename(columns={"Date": "date","Open": "open","High": "high","Low": "low","Close": "close","Volume": "vol",},inplace=True,)
    vti['VTI'] = vti['close']
    vti = vti[~np.isnan(vti['VTI'])]

    while finance_list:
        symbol = finance_list[0]
        data_source = dict_data[dict_data["Symbol"] == symbol].values[0][5]
        if data_source == '-' or symbol == '-':
            finance_list.pop(0)
            continue
        if data_source == 'own':
            # print('更新own金融数据')
            symbol_names = symbol.split("/")
            data_1 = sql_data.readDB(finance_db, symbol_names[0])
            data_1.sort_index(inplace=True)
            data_2 = sql_data.readDB(finance_db, symbol_names[1])
            data_2.sort_index(inplace=True)
            data_1[symbol] = data_1[symbol_names[0]] / data_2[symbol_names[1]]
            data = analysis.updateFinanceData(symbol,vti, data_1)
            sql_data.dataToDB(finance_db, data_1, symbol)
            finance_list.pop(0)
            continue
        # 从数据库中读取table
        old_data = sql_data.readDB(finance_db, symbol)
        if old_data is not None:
            # old_data['date'] = pd.to_datetime(old_data['date'])
            try:
                last_day = dt.datetime.strptime(old_data['date'].values[-1] , '%Y-%m-%d')
            except :
                last_day = dt.datetime.strptime(old_data['date'].values[-1] , '%Y-%m-%d %H:%M:%S')


            # last_day = old_data['date'].values[-1].astype(dt.datetime)
            
            # last_day=last_day.to_datetime()
            if last_day < yesterday :
                new_df = download(code=symbol, start=last_day, end=yesterday, source=data_source)
                last_trad_day = new_df.index[-1].to_pydatetime()
                if last_trad_day > last_day:
                    print('更新金融数据')
                    data = analysis.updateFinanceData(symbol,vti,new_df,old_data)
                    sql_data.dataToDB(finance_db, data, symbol)
        # 创建新数据
        else:
            print('创建金融数据')
            data = download(symbol, start=start, end=end, source=data_source)
            if data is not None :
                data = analysis.updateFinanceData(symbol,vti, data)
                sql_data.dataToDB(finance_db, data, symbol)
        print(symbol, data_source,  last_trad_day)
        finance_list.pop(0)


def getSpxInfo():
    spx_1 = stock_info.get_spx()
    spx_2 = stock_info.get_spx2()
    ndx = stock_info.get_ndx()
    dji = stock_info.get_dji()
    # 重写column
    spx_1 = spx_1.reindex(columns=['code', 'name', 'is_spx', 'sp_sector'])
    spx_1['code'] = spx_1['code'].str.replace('.', '-')
    spx_2 = spx_2.reindex(columns=['code', 'name', 'spx_weight'])
    spx_2['code'] = spx_2['code'].str.replace('.', '-')
    ndx = ndx.reindex(columns=['code', 'name', 'is_ndx', 'ndx_weight'])
    ndx['code'] = ndx['code'].str.replace('.', '-')
    dji = dji.reindex(columns=['code', 'name', 'is_dji', 'dji_weight'])
    dji['code'] = dji['code'].str.replace('.', '-')
    # 重排索引
    spx_1.set_index(["code"], inplace=True)
    spx_2.set_index(["code"], inplace=True)
    ndx.set_index(["code"], inplace=True)
    dji.set_index(["code"], inplace=True)
    spx_1.sort_index(inplace=True)
    spx_2.sort_index(inplace=True)
    ndx.sort_index(inplace=True)
    dji.sort_index(inplace=True)
    # 合并
    spx_1['spx_weight'] = spx_2['spx_weight']
    spx_1['is_ndx'] = ndx['is_ndx']
    spx_1['ndx_weight'] = ndx['ndx_weight']
    spx_1['is_dji'] = dji['is_dji']
    spx_1['dji_weight'] = dji['dji_weight']
    # reset 索引
    spx_1.reset_index(inplace=True)
    spx_db = '{}/datas/db/{}.db'.format(path, config.get('database', 'spx'))
    sql_data.dataToDB(spx_db, spx_1, config.get('tablename', 'sxp'))

def updateMarketBreadthToDB():
    # 读取spxDB
    spx_db = '{}/datas/db/{}.db'.format(path, config.get('database', 'spx'))
    stocks_db = '{}/datas/db/{}.db'.format(path,config.get('database', 'stocks'))
    spx = sql_data.readDB(spx_db, 'spx')
    stock_list = spx["code"].tolist()
    datas = sql_data.readDB(stocks_db, stock_list)

    spx_info_data = sql_data.readDB(spx_db, 'spx')
    column_label = list(sp500_dict.keys())
    start = date.get_3year_ago()
    end = date.now()
    row_index = pd.date_range(start=start, end=end, freq='D')
    df = pd.DataFrame(0, index=row_index, columns=column_label)
    while datas:
        data = datas[0]
        data = data.set_index(["date"]).sort_index()
        data.index = pd.to_datetime(data.index)
        industry = spx_info_data.loc[spx_info_data['code'] == data['code'].values[0]]['sp_sector'].values[0]
        df[industry] += data['is_above_s_ma']
        datas.pop(0)
    print(df)
    df = analysis.market_breadth_analysis(spx_info_data, df)
    # 保存marketDB
    market_breadth_db = '{}/datas/db/{}.db'.format(path, config.get('database', 'market_breadth'))
    sql_data.dataToDB(market_breadth_db, df, config.get('tablename', 'market_breadth'))


def updateStockToDB():
    spx_db = '{}/datas/db/{}.db'.format(path, config.get('database', 'spx'))
    stocks_db = '{}/datas/db/{}.db'.format(path,config.get('database', 'stocks'))
    spx = sql_data.readDB(spx_db, 'spx')
    stock_list = spx["code"].tolist()
    start = date.get_year_ago()
    end = date.now()
    yesterday = dt.datetime.strptime(date.get_yesterday() , '%Y-%m-%d')
    last_trad_day = date.get_current_day()
    datas = sql_data.readDB(stocks_db, stock_list)
    stock_datas = []
    if datas and isinstance(datas,list):
        # 更新股票
        while datas:
            df = datas[0]
            last_day = dt.datetime.strptime(df['date'].values[-1] , '%Y-%m-%d')
            code = df['code'].values[0]
            print(code, last_day, last_trad_day)
            if last_day < yesterday and last_trad_day != last_day:
                print('更新：',code)
                new_df = download(code=code, start=last_day, end=yesterday, source='yahoo')
                last_trad_day = new_df.index[-1].to_pydatetime()
                # 如果不是最新时间则更新DB
                new_df = new_df.reset_index()
                new_df.rename(columns={"Date": "date","Open": "open","High": "high","Low": "low","Close": "close","Volume": "vol",},inplace=True,)
                new_df = new_df[~np.isnan(new_df["close"])]
                new_df.drop(['Adj Close'],inplace=True,axis=1)
                # 重设index为str，为concat准备
                new_df[["date"]] = new_df[["date"]].astype(str)
                # 连接df
                final_data = pd.concat([df.set_index(["date"]).sort_index(),new_df.set_index(["date"]).sort_index()])
                # 删除重复的index           
                final_data = final_data[~final_data.index.duplicated(keep='last')]
                final_data['code'] = final_data['code'].values[0]
                final_data = analysis.stock_analysis(final_data,20,60,120)
                # print(final_data.tail(5))
                stock_datas.append(final_data)
            datas.pop(0)
    else:
        # 创建股票数据
        while stock_list:
            symbol = stock_list[0]
            data = download(code=symbol, start=start, end=end, source="yahoo")
            if data is not None :
                data["code"] = symbol
                stock_datas.append(analysis.stock_analysis(data,20,60,120))
                stock_list.pop(0)
                print('>{0}完成，还剩{1}'.format(symbol, len(stock_list)))
    # 写入数据库
    if stock_datas or len(stock_datas)>0:
        sql_data.dataToDB(stocks_db,stock_datas,None)


def update_data():
    updateFinanceToDB()
    updateStockToDB()
    updateMarketBreadthToDB()





if __name__ == '__main__':

    # updateStockToDB()
    createDictToDB()
    # update_data()
    # getSpxInfo()
    # createMarketBreadthToDB()
    # market_breadth_db = '{}/datas/db/{}.db'.format(path, config.get('database','market_breadth'))
    # spx_db = '{}/datas/db/{}.db'.format(path, config.get('database','spx'))
    # df =sql_data.readDB(market_breadth_db, config.get('tablename','market_breadth'))
    # print(df)
    # spx_info_data = sql_data.readDB(spx_db, 'spx')
