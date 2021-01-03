# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
import os, sys
path=os.path.abspath('.')   
sys.path.append(path)
from datas import sql_data
from config.config import *


table_1 = 'TREAST'
table_2 = 'FEDDT'
table_3 = 'WSHOMCB'
table_4 = 'SWPT'

financeDB = '{}/datas/db/{}.db'.format(path, config.get('database','finance'))
treast = sql_data.readDB(financeDB, table_1)
feddt = sql_data.readDB(financeDB, table_2)
wshomcb = sql_data.readDB(financeDB, table_3)
swpt = sql_data.readDB(financeDB, table_4)

dictDB = '{}/datas/db/{}.db'.format(path, config.get('database','data_dict'))
dictDF =sql_data.readDB(dictDB, config.get('tablename','data_dict'))

info1 = dictDF.loc[dictDF['Symbol'] == table_1]['Introduc'].values[0]
info2 = dictDF.loc[dictDF['Symbol'] == table_2]['Introduc'].values[0]
info3 = dictDF.loc[dictDF['Symbol'] == table_3]['Introduc'].values[0]
info4 = dictDF.loc[dictDF['Symbol'] == table_4]['Introduc'].values[0]


fed_assets_graph = dcc.Graph(
    figure=dict(
        data=[
            dict(
                x=treast['date'],
                y=treast[table_1],
                name=info1,
                line=dict(width=1, color='Lavender'),
                type='scatter',
                fill='tozeroy',
            ),
            dict(
                x=feddt['date'],
                y=feddt[table_2],
                name=info2,
                line=dict(width=1,color='Thistle',),  # dash='dot' 虚线
                fill='tozeroy',  # 填充
            ),
            dict(
                x=wshomcb['date'],
                y=wshomcb[table_3],
                name=info3,
                line=dict(width=1,color='Orchid',),  # dash='dot' 虚线
                fill='tozeroy',  # 填充
            ),
        ],
        layout=dict(
            title='Fed System Open Market Holdings',
            xaxis=dict(rangeslider=dict(bgcolor='transparent'),),
            yaxis=dict(fixedrange=True,side='left',),
            autosize=True,
            # 透明bgcolor
            paper_bgcolor='transparent',
            plot_bgcolor='transparent',
            # 不显示图例
            showlegend=False,
            legend=dict(x=0, y=1.0),
            margin=dict(l=20, r=20, t=40, b=40)),
    ),
    style={
        'height': 500,
        'width': "100%"
    },
    config={
        'responsive': True,
        'autosizable': True,
        'showAxisDragHandles': True,
        'staticPlot': False,  # 静态图
        'displayModeBar': False  # 关闭工具箱
    },
    id='fed_assets_graph',
    responsive='auto')

liq_swap_graph = dcc.Graph(
    figure=dict(
        data=[
            dict(
                x=swpt['date'],
                y=swpt[table_4],
                name=info4,
                type='bar',
            ),
        ],
        layout=dict(
            title='Central Bank Liquidity Swaps',
            xaxis=dict(rangeslider=dict(bgcolor='transparent'),),
            yaxis=dict(fixedrange=True,side='left',),
            autosize=True,
            # 透明bgcolor
            paper_bgcolor='transparent',
            plot_bgcolor='transparent',
            # 不显示图例
            showlegend=False,
            legend=dict(x=0, y=1.0),
            margin=dict(l=20, r=20, t=40, b=40)),
    ),
    style={
        'height': 500,
        'width': "100%"
    },
    config={
        'responsive': True,
        'autosizable': True,
        'showAxisDragHandles': True,
        'staticPlot': False,  # 静态图
        'displayModeBar': False  # 关闭工具箱
    },
    id='swpt_graph',
)

page = html.Div(children=[fed_assets_graph,
                          html.Hr(), liq_swap_graph],
                className="container")
