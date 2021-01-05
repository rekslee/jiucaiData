# -*- coding: utf-8 -*-

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_daq as daq
import os
from datas import sql_data
from config.config import *
import pandas as pd

path=os.path.abspath('.') 
dictDF = pd.read_csv(path + "/config/financial_data_dict.csv")

def graph(df, table,linecolor='#34495E',bgcolor='transparent'):
    line_color = linecolor
    bg_color = bgcolor
    return dcc.Graph(
        figure=dict(
            data=[
                dict(
                    x=df['date'],
                    y=df[table],
                    type='line',
                    line=dict(width=2, color=line_color),
                ),
            ],
            layout=dict(
                paper_bgcolor= bg_color,
                plot_bgcolor='transparent',
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                showlegend=False,
                legend=dict(x=0, y=1.0),
                uirevision = True,
                margin=dict(l=0, r=0, t=4, b=4),
            ),
        ),
        style={"width": "100px", "height": "40px"},
        config={'staticPlot': False, "editable": False, 'displayModeBar': False},
        id=table,
    )

def badge(num):
    float(num)
    if num < 0:
        return html.P(dbc.Badge('{}%'.format(num), color="danger", pill=True, className="mr-1"))
    elif num == 0:
        return html.P(dbc.Badge('{}%'.format(num), color="warning", pill=True, className="mr-1"))
    else:
        return html.P(dbc.Badge('{}%'.format(num), color="success", pill=True, className="mr-1"))



def indicator(cur_price, pre_price):
    if cur_price > pre_price:
        return daq.Indicator(color="green",size=10)
    elif cur_price == pre_price:
        return daq.Indicator(color="violet",size=10)
    else:
        return daq.Indicator(color="red",size=10)

def item(index, name, pcd, introduc, cur_price,pre_price, graph1,graph2=''):
    
    return dbc.Col([dbc.Row([
            dbc.Col(html.H6(name,className="col",id='name{}'.format(index)),width=3),
            dbc.Tooltip(introduc,target="name{}".format(index),placement="left"),
            dbc.Col([html.H4(pre_price),badge(pcd)], align="end",width=2),
            dbc.Col(indicator(cur_price,pre_price),width=1),
            dbc.Col(html.Div(graph1),width=3),
            dbc.Col(html.Div(graph2),width=3),
        ],align="center",justify="between",),html.Hr()])

def list_item(symbol_list,dictDF,datas):
    mac=[]
    sup=[]
    ris=[]
    rat=[]
    cur=[]
    ene=[]
    pre=[]
    met=[]
    fun=[]
    agr=[] 
    bro=[]
    fac=[]
    gro=[]
    the=[]
    ind=[]
    for i in range(len(symbol_list)):
        symbol = symbol_list[i]
        data = datas[i]
        name = dictDF.loc[dictDF['Symbol']==symbol]['Name'].values[0]
        introduc = dictDF.loc[dictDF['Symbol']==symbol]['Introduc'].values[0]
        category = dictDF.loc[dictDF['Symbol']==symbol]['Category'].values[0]
        pcd = data['5dpc'].round(3).values[-1]
        cur_price = data[symbol].round(3).values[-1]
        pre_price = data[symbol].round(3).values[-2]
        if category == 'Rates&Yields':
            rat.append(dbc.Col(item(i,name, pcd, introduc, cur_price, pre_price, '', graph(data,symbol)), width=4))
        if category == 'Macro':
            mac.append(dbc.Col(item(i,name, pcd, introduc, cur_price, pre_price, '', graph(data,symbol)), width=4))
        if category == 'Risk Gauges':
            ris.append(dbc.Col(item(i,name, pcd, introduc, cur_price, pre_price, '', graph(data,symbol)), width=4))
        if category == 'Supply & Demand':
            sup.append(dbc.Col(item(i,name, pcd, introduc, cur_price, pre_price, '', graph(data,symbol)), width=4))
        if category == 'Currency':
            cur.append(dbc.Col(item(i,name, pcd, introduc, cur_price, pre_price, '', graph(data,symbol)), width=4))
        if category == 'Energy':
            ene.append(dbc.Col(item(i,name, pcd, introduc, cur_price, pre_price, '', graph(data,symbol)), width=4))
        if category == 'Precious':
            pre.append(dbc.Col(item(i,name, pcd, introduc, cur_price, pre_price, '', graph(data,symbol)), width=4))
        if category == 'Metal':
            met.append(dbc.Col(item(i,name, pcd, introduc, cur_price, pre_price, '', graph(data,symbol)), width=4))
        if category == 'Fundamental':
            fun.append(dbc.Col(item(i,name, pcd, introduc, cur_price, pre_price, '', graph(data,symbol)), width=4))
        if category == 'Agriculture':
            agr.append(dbc.Col(item(i,name, pcd, introduc, cur_price, pre_price, '', graph(data,symbol)), width=4))
        if category == 'Broad Market':
            bro.append(dbc.Col(item(i,name, pcd, introduc, cur_price, pre_price, graph(data,symbol),graph(data,'rel',linecolor='Orange')), width=4))
        if category == 'Factors':
            fac.append(dbc.Col(item(i,name, pcd, introduc, cur_price, pre_price, graph(data,symbol),graph(data,'rel',linecolor='Orange')), width=4))
        if category == 'Growth or Value':
            gro.append(dbc.Col(item(i,name, pcd, introduc, cur_price, pre_price, graph(data,symbol),graph(data,'rel',linecolor='Orange')), width=4))
        if category == 'Thematic':
            the.append(dbc.Col(item(i,name, pcd, introduc, cur_price, pre_price, graph(data,symbol),graph(data,'rel',linecolor='Orange')), width=4))
        if category == 'Industry':
            ind.append(dbc.Col(item(i,name, pcd, introduc, cur_price, pre_price, graph(data,symbol),graph(data,'rel',linecolor='Orange')), width=4))
    col_items = []
    col_items.append(dbc.Col([dbc.Col(dbc.Alert(html.H4('Macro 宏观数据'), color="success"), width=4),dbc.Row(mac)]))
    col_items.append(dbc.Col([dbc.Col(dbc.Alert(html.H4('Rates&Yields 利率与收益'), color="primary"), width=4),dbc.Row(rat)]))
    col_items.append(dbc.Col([dbc.Col(dbc.Alert(html.H4('Risk Gauges 风险指数'), color="warning"), width=4),dbc.Row(ris)]))
    col_items.append(dbc.Col([dbc.Col(dbc.Alert(html.H4('Fundamental 基本面'), color="warning"), width=4),dbc.Row(fun)]))
    col_items.append(dbc.Col([dbc.Col(dbc.Alert(html.H4('Supply&Demand 需求与供给' ), color="danger"), width=4),dbc.Row(sup)]))
    col_items.append(dbc.Col([dbc.Col(dbc.Alert(html.H4('Currency 货币板块'), color="info"), width=4),dbc.Row(cur)]))
    col_items.append(dbc.Col([dbc.Col(dbc.Alert(html.H4('Energy 能源板块'), color="dark"), width=4),dbc.Row(ene)]))
    col_items.append(dbc.Col([dbc.Col(dbc.Alert(html.H4('Precious 贵金属板块'), color="primary"), width=4),dbc.Row(pre)]))
    col_items.append(dbc.Col([dbc.Col(dbc.Alert(html.H4('Metal 金属板块'), color="success"), width=4),dbc.Row(met)]))
    col_items.append(dbc.Col([dbc.Col(dbc.Alert(html.H4('Agriculture 农业板块'), color="danger"), width=4),dbc.Row(agr)]))
    col_items.append(dbc.Col([dbc.Col(dbc.Alert(html.H4('Index Market 市场指数'), color="info"), width=4),dbc.Row(bro)]))
    col_items.append(dbc.Col([dbc.Col(dbc.Alert(html.H4('Factors 因子ETF'), color="dark"), width=4),dbc.Row(fac)]))
    col_items.append(dbc.Col([dbc.Col(dbc.Alert(html.H4('Growth&or&Value 成长型与价值型ETF'), color="primary"), width=4),dbc.Row(gro)]))
    col_items.append(dbc.Col([dbc.Col(dbc.Alert(html.H4('Thematic 专题板块'), color="success"), width=4),dbc.Row(the)]))
    col_items.append(dbc.Col([dbc.Col(dbc.Alert(html.H4('Industry 行业板块'), color="dark"), width=4),dbc.Row(ind)]))
    return col_items

symbol_list = dictDF.loc[(dictDF['Display']=='y') &(dictDF['Symbol']!='-')]['Symbol'].tolist()
symbol_list2 = dictDF.loc[(dictDF['Display']=='y') &(dictDF['Symbol']!='-')]['Symbol'].tolist()

financeDB = '{}/datas/db/{}.db'.format(path, config.get('database','finance'))
datas = sql_data.readDB(financeDB,symbol_list,-30)


page = html.Div(
    # className="container",
    children=list_item(symbol_list2,dictDF,datas))
