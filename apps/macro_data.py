# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# import dash
# import dash_daq as daq
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import os, sys
path=os.path.abspath('.')   #表示当前所处的文件夹的绝对路径
sys.path.append(path)
from datas import sql_data, analysis
from config.config import *
financeDB = '{}/datas/db/{}.db'.format(path, config.get('database','finance'))
dictDB = '{}/datas/db/{}.db'.format(path, config.get('database','data_dict'))
dictDF =sql_data.readDB(dictDB, config.get('tablename','data_dict'))


table_1 = 'CCSA'
table_2 = 'ICSA'
table_3 = 'WEI'
table_4 = 'DGS10'
table_5 = 'DGS5'
table_6 = 'EFFR'
table_7 = 'CPIAUCSL'
table_8 = '^TNX'  # 10年期国债收益
table_9 = 'HG=F/GC=F'  # 铜
table_10 = 'CL=F/GC=F'  # 原油
introduc1 = dictDF.loc[dictDF['Symbol'] == table_1]['Introduc'].values[0]
introduc2 = dictDF.loc[dictDF['Symbol'] == table_2]['Introduc'].values[0]
introduc3 = dictDF.loc[dictDF['Symbol'] == table_3]['Introduc'].values[0]
introduc4 = dictDF.loc[dictDF['Symbol'] == table_4]['Introduc'].values[0]
introduc5 = dictDF.loc[dictDF['Symbol'] == table_5]['Introduc'].values[0]
introduc6 = dictDF.loc[dictDF['Symbol'] == table_6]['Introduc'].values[0]
introduc7 = dictDF.loc[dictDF['Symbol'] == table_7]['Introduc'].values[0]
introduc8 = dictDF.loc[dictDF['Symbol'] == table_8]['Introduc'].values[0]
introduc9 = dictDF.loc[dictDF['Symbol'] == table_9]['Introduc'].values[0]
introduc10 = dictDF.loc[dictDF['Symbol'] == table_10]['Introduc'].values[0]
Explanation1 = dictDF.loc[dictDF['Symbol'] == table_1]['Explanation'].values[0]
Explanation2 = dictDF.loc[dictDF['Symbol'] == table_2]['Explanation'].values[0]
Explanation3 = dictDF.loc[dictDF['Symbol'] == table_3]['Explanation'].values[0]
Explanation9 = dictDF.loc[dictDF['Symbol'] == table_9]['Explanation'].values[0]
Explanation10 = dictDF.loc[dictDF['Symbol'] == table_10]['Explanation'].values[0]


# 失业数据
ccsa = sql_data.readDB(financeDB, table_1)
icsa = sql_data.readDB(financeDB, table_2)
# 经济指数
wei = sql_data.readDB(financeDB, table_3)
# 联储收益率
dgs10 = sql_data.readDB(financeDB, table_4)
dgs5 = sql_data.readDB(financeDB, table_5)
# 利率&CPI
effr = sql_data.readDB(financeDB, table_6)
cpi = sql_data.readDB(financeDB, table_7)
us10YY = sql_data.readDB(financeDB, table_8)
cg = sql_data.readDB(financeDB, table_9)
og = sql_data.readDB(financeDB, table_10)
# CPI同比
cpi['CPI(YoY)'] = cpi[table_7].diff()
cg.dropna(inplace=True)
og.dropna(inplace=True)

effr = analysis.set_time_series(effr)
cpi = analysis.set_time_series(cpi)
effr=effr.round(1)
cpi=cpi.round(2)
jobless_data_graph = dcc.Graph(
    figure=dict(
        data=[
            dict(x=ccsa['date'],
                 y=ccsa[table_1],
                 name=introduc1,
                 line=dict(width=1, color='pink'),
                 type='scatter',
                 fill='tozeroy',
                 yaxis='y',
                 facet_col="species"),
            dict(
                x=icsa['date'],
                y=icsa[table_2],
                name=introduc2,
                line=dict(
                    width=1,
                    color='skyblue',
                ),  # dash='dot' 虚线
                fill='tozeroy',  # 填充
                yaxis='y2',
            ),
        ],
        layout=dict(
            title='US.Jobless Data',
            xaxis=dict(rangeslider=dict(bgcolor='transparent')),
            yaxis=dict(fixedrange=True,side='left',),
            yaxis2=dict(side='right', overlaying='y',visible=False),
            autosize=True,
            # 透明bgcolor
            paper_bgcolor='transparent',
            plot_bgcolor='transparent',
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
    id='jobless_graph',
    responsive='auto')

wei_graph = dcc.Graph(
    figure=dict(
        data=[
            dict(
                x=wei['date'],
                y=wei[table_3],
                name=introduc3,
                line=dict(width=2, color='DimGray'),
            ),
        ],
        layout=dict(
            title='Weekly Economic Index',
            responsive=True,
            autosize=True,
            yaxis=dict(fixedrange=True),
            xaxis=dict(rangeslider=dict(bgcolor='transparent')),
            # 透明bgcolor
            paper_bgcolor='transparent',
            plot_bgcolor='transparent',
            legend=dict(x=0, y=1.0),
            margin=dict(l=20, r=20, t=40, b=40)),
    ),
    style={
        'height': 500,
        'width': "100%"
    },
    config={
        # 'scrollZoom': True,
        'responsive': True,
        'autosizable': True,
        'showAxisDragHandles': True,
        'staticPlot': False,  # 静态图
        'displayModeBar': False  # 关闭工具箱
    },
    id='wei_graph',
)

treasury_graph = dcc.Graph(
    figure=dict(
        data=[
            dict(
                x=dgs10['date'],
                y=dgs10[table_4],
                name=introduc4,
                line=dict(width=1, color='Pink'),
                yaxis='y',
            ),
            dict(
                x=dgs5['date'],
                y=dgs5[table_5],
                name=introduc5,
                line=dict(
                    width=1,
                    color='SkyBlue',
                ),  # dash='dot' 虚线
                yaxis='y',
            ),
            dict(
                x=effr['date'],
                y=effr[table_6],
                name=introduc6,
                line=dict(
                    width=1,
                    color='Black',
                ),  # dash='dot' 虚线
                yaxis='y2',
            ),
            dict(
                x=cpi['date'],
                y=cpi['CPI(YoY)'],
                name=introduc7,
                line=dict(
                    width=1,
                    color='Gray',
                ),  # dash='dot' 虚线
                yaxis='y2',
            ),
        ],
        layout=dict(
            title='Treasury Yield & CPI(YoY) & Fed Rate',
            xaxis=dict(
                rangeslider=dict(bgcolor='transparent'),
                ),
            yaxis=dict(fixedrange=True),
            yaxis2=dict(fixedrange=True,side='right', overlaying='y',visible=False),
            autosize=True,
            # 透明bgcolor
            paper_bgcolor='transparent',
            plot_bgcolor='transparent',
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
    id='treasury_yield_graph',
)

abstract_graph = dcc.Graph(
    figure=dict(
        data=[
            dict(
                x=us10YY['date'],
                y=us10YY[table_8],
                name=introduc8,
                line=dict(width=1, color='DimGray'),
            ),
            dict(
                x=us10YY['date'],
                y=cg[table_9],
                yaxis='y2',
                name=introduc9,
                line=dict(
                    width=1,
                    color='Gold',
                ),  # dash='dot' 虚线
            ),
            dict(
                x=us10YY['date'],
                y=og[table_10],
                yaxis='y3',
                name=introduc10,
                line=dict(
                    width=1,
                    color='YellowGreen',
                ),  # dash='dot' 虚线
            ),
        ],
        layout=dict(
            title='Abstract Macro',
            xaxis=dict(rangeslider=dict(bgcolor='transparent'),),
            yaxis=dict(fixedrange=True,),
            yaxis2=dict(fixedrange=True,side='right', overlaying='y',visible=False),
            yaxis3=dict(fixedrange=True,side='right',overlaying='y',visible=False),
            responsive=True,
            autosize=True,
            # 透明bgcolor
            paper_bgcolor='transparent',
            plot_bgcolor='transparent',
            legend=dict(x=0, y=1.0),
            margin=dict(l=20, r=20, t=40, b=40),
        ),
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
    id='abstract_macro_graph',
)

def card_content(data,title,body):
    return [
    dbc.CardHeader(title),
    dbc.CardBody(
        [
            html.H3(data, className="card-title"),
            html.P(body,className="card-text",),
        ]
    ),
    
]

page = dbc.Col([
        dbc.Row(
            [   dbc.Col(dbc.Card(card_content(str(icsa[table_2].values[-1]/10000)+'（万人）',introduc2,Explanation1), color="primary", inverse=True,style={"width": "16rem"},), width=2),
                dbc.Col(dbc.Card(card_content(str(ccsa[table_1].values[-1]/10000)+'（万人）',introduc1,Explanation2), color="danger", inverse=True,style={"width": "16rem"},), width=2),
                dbc.Col(dbc.Card(card_content(wei[table_3].values[-1],introduc3,Explanation3), color="dark", inverse=True,style={"width": "16rem"},), width=2),
                dbc.Col(dbc.Card(card_content(cg[table_9].round(3).values[-1],introduc9,Explanation9), color="warning", inverse=True,style={"width": "16rem"},), width=2),
                dbc.Col(dbc.Card(card_content(og[table_10].round(3).values[-1],introduc10,Explanation10), color="success", inverse=True,style={"width": "16rem"},), width=2),
            ],justify="between",),
        html.Div(
            [
                html.Hr(),jobless_data_graph,
                html.Hr(),wei_graph,
                html.Hr(),abstract_graph,
                html.Hr(),treasury_graph,
            ],className="container")
            ])
