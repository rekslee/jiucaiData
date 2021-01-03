# -*- coding:utf-8 -*-
"""
code from https://github.com/bankrollhunter/market-breadt
"""
import numpy as np
import pandas as pd


def stock_ma(data, short, mid, long):
    data = data.set_index(["date"]).sort_index()
    # close = data.close.values
    data.loc[:, "s_ma"] = data["close"].rolling(short).mean()
    data.loc[:, "m_ma"] = data["close"].rolling(mid).mean()
    data.loc[:, "l_ma"] = data["close"].rolling(long).mean()

    data.loc[:, "s_ema"] = data["close"].ewm(span=short, adjust=False).mean()
    data.loc[:, "m_ema"] = data["close"].ewm(span=mid, adjust=False).mean()
    data.loc[:, "l_ema"] = data["close"].ewm(span=long, adjust=False).mean()

    data.loc[:, "cs"] = (data["close"] - data["s_ma"]) / data["s_ma"] * 100
    data.loc[:, "sm"] = (data["s_ma"] - data["m_ma"]) / data["m_ma"] * 100
    data.loc[:, "ml"] = (data["m_ma"] - data["l_ma"]) / data["l_ma"] * 100
    data.loc[:, "bais"] = data["cs"] + data["sm"] + data["ml"]

    data.loc[:, "ecs"] = (data["close"] - data["s_ema"]) / data["s_ema"] * 100
    data.loc[:, "esm"] = (data["s_ema"] - data["m_ema"]) / data["m_ema"] * 100
    data.loc[:, "eml"] = (data["m_ema"] - data["l_ema"]) / data["l_ema"] * 100
    data.loc[:, "ebais"] = data["ecs"] + data["esm"] + data["eml"]
    return data.reset_index()


def stock_vol(data, short):
    data = data.set_index(["date"]).sort_index()
    # data['vol'] = data['vol'].replace(np.nan, 0)
    # vol = data.vol.values
    # vol = vol.astype(float)
    data.loc[:, "ma_vol"] = data["vol"].rolling(short).mean()
    data.loc[:, "vol_rate"] = data["vol"] / data["ma_vol"]
    return data.reset_index()


def is_gap(h, l, c, p_h, p_l, p_c):
    if c is None or p_c is None:
        return "N"
    elif c > p_c:
        return "Y" if l > p_h else "N"
    else:
        return "Y" if h < p_l else "N"


def is_over(x, px):
    if x is None or px is None:
        return "N"
    elif x > 0 and px < 0:
        return "Y"
    else:
        return "N"


def stock_gap_and_over(data):
    data[["date"]] = data[["date"]].astype(str)
    data["row_num"] = data.date.rank(method="min").astype(int)
    data_copy = data.copy()
    data_copy.row_num = data_copy.row_num.apply(lambda x: x + 1)
    data_copy.rename(
        columns={"open": "pre_open","high": "pre_high","low": "pre_low","close": "pre_close","cs": "pcs","sm": "psm","ml": "pml","ecs": "pecs","esm": "pesm","eml": "peml",},
        inplace=True,
    )
    data_copy = data_copy[["code","row_num","pre_open","pre_high","pre_low","pre_close","pcs","psm","pml","pecs","pesm","peml",]]
    data = data.set_index(["code", "row_num"])
    data_copy = data_copy.set_index(["code", "row_num"])
    data = pd.merge(data, data_copy, how="left", on=["code", "row_num"])
    # print(data)
    data["is_gap"] = data.apply(lambda row: is_gap(row["high"],row["low"],row["close"],row["pre_high"],row["pre_low"],row["pre_close"],),axis=1,)
    data["is_esm_over"] = data.apply(lambda row: is_over(row["esm"], row["pesm"]), axis=1)
    data["is_eml_over"] = data.apply(lambda row: is_over(row["eml"], row["peml"]), axis=1)
    data["is_cs_over"] = data.apply(lambda row: is_over(row["cs"], row["pcs"]), axis=1)
    data["is_sm_over"] = data.apply(lambda row: is_over(row["sm"], row["psm"]), axis=1)
    data["is_ml_over"] = data.apply(lambda row: is_over(row["ml"], row["pml"]), axis=1)
    return data.reset_index()


def is_turn_up(c, p_c, c_ago, p_c_ago):
    if p_c_ago is None or c_ago is None:
        return "N"
    elif c > c_ago and p_c < p_c_ago:
        return "Y"
    else:
        return "N"


def stock_turn_up(data, c, day):
    data[["date"]] = data[["date"]].astype(str)
    data["row_num"] = data.date.rank(method="min").astype(int)
    data_copy = data.copy()
    data_copy.row_num = data_copy.row_num.apply(lambda x: x + day)
    close_ago = "{}_close".format(c)
    pre_close_ago = "{}_pre_close".format(c)
    data_copy.rename(columns={"close": close_ago, "pre_close": pre_close_ago}, inplace=True)
    data_copy = data_copy[["code", "row_num", close_ago, pre_close_ago]]
    data = data.set_index(["code", "row_num"])
    data_copy = data_copy.set_index(["code", "row_num"])
    data = pd.merge(data, data_copy, how="left", on=["code", "row_num"])

    column = "is_{}_up".format(c)
    data[column] = data.apply(lambda row: is_turn_up(row["close"], row["pre_close"], row[close_ago], row[pre_close_ago]),axis=1)
    return data.reset_index()

def market_breadth_analysis(spx_info,data):
    spSector = spx_info['sp_sector'].value_counts().to_dict()
    data.sort_index(ascending=False, inplace=True)
    data.dropna(inplace=True)
    # data.set_index('date',drop=True,inplace=True)
    keys = data.columns.tolist()
    if 'date' in keys:
        keys.remove('date')
    if 'total' in keys:
        keys.remove('total')

    for key in keys:
        data[key] = (data[key]/spSector[key]*100).round(0).astype(int)
    data["total"] = data.sum(axis=1)
    data['date'] = pd.to_datetime(data.index, format="%Y-%m-%d")
    
    return data

def stock_analysis(data, short=20, mid=60, long=120):
    # if data is None or data.empty or data.date.size < long + 1:
    #     return None
    data.sort_index(inplace=True)
    data = data.reset_index()
    data.rename(columns={"Date": "date","Open": "open","High": "high","Low": "low","Close": "close","Volume": "vol",},inplace=True,)
    data = data[~np.isnan(data["close"])]
    stk_columns = ["date", "code", "open", "high", "low", "close", "vol"]
    data = data[stk_columns]
    data = stock_ma(data, short, mid, long)
    data = stock_vol(data, short)
    data = stock_gap_and_over(data)
    data = stock_turn_up(data, "s", short)
    data = stock_turn_up(data, "m", mid)
    data = stock_turn_up(data, "l", long)
    data['is_above_s_ma']= (data['close']>data['s_ma']).astype(int)
    
    return data

def updateFinanceData(code,vti,data,old_data=None):
    
    data = data.reset_index()
    # 如果不是ferd数据
    if code not in data.columns:
        if 'Adj Close' in data.columns:
            data.drop('Adj Close',inplace=True,axis=1)
        data.rename(columns={"Date": "date","Open": "open","High": "high","Low": "low","Close": "close","Volume": "vol",},inplace=True,)
        data[code]=data['close']
        data = data[~np.isnan(data[code])]
        data['rel'] = data['close'] / vti['close']
    else:
        data.rename(columns={"DATE": "date"},inplace=True,)
        data = data[~np.isnan(data[code])]
    if old_data is not None :
        old_data.sort_index(inplace=True)
        data = pd.concat([old_data.set_index('date'),data.set_index('date')])
        # print(data)
      
        data.index = pd.to_datetime(data.index)
        data.sort_index(inplace=True)
        data.index = data.index.astype(str)
        data = data[~data.index.duplicated(keep='last')]
        data = data.reset_index()
    data['5dpc'] = data[code].pct_change(5).round(5)*100
    print(data.tail(5))
    return data

def set_time_series(data):
    data['date'] = pd.to_datetime(data['date'], format="%Y-%m-%d")
    data = data.set_index(data['date'])
    data = data.reindex(pd.date_range(data['date'].values[0],data['date'].values[-1]))
    data.fillna(method='ffill', inplace=True)
    data['date'] = pd.to_datetime(data.index, format="%Y-%m-%d")
    return data