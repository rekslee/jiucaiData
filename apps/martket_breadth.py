# -*- coding: utf-8 -*-

import dash_html_components as html
import copy
import dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import os
from datas import sql_data, symbol_data
from config.config import *

path=os.path.abspath('.') 
col = symbol_data.sp500_dict
col['date'] = 'Date 日期'
col['total'] = 'Total 总数'
market_breadthDB = '{}/datas/db/{}.db'.format(path, config.get('database','market_breadth'))
df =sql_data.readDB(market_breadthDB, config.get('tablename','market_breadth'))
df['date'] = pd.to_datetime(df['date'],format='%Y-%m-%d')
df['date'] = df.date.dt.strftime('%Y-%m-%d')


def table_style(df):
    styles = []
    for col in df.columns:
        num = 100
        t = 1
        if col == 'total':
            num = 1100
        x = copy.deepcopy(num)
        for j in range(1, 22):
            if t<0.1:
                t = round(t+0.09,2)
            if num >= x/2:
                styles.append({
                        'if': {
                            'filter_query':'{{{col}}} >= {mix} && {{{col}}} < {max}'.format(col=col, mix=num, max=num+x/20),
                            'column_id':col
                        },
                        'backgroundColor':'rgba(40, 180, 99  ,{})'.format(t),
                        'color':'MidnightBlue',
                        'border': '0px solid rgba(40, 180, 99  ,{})'.format(t),
                    })
                t = round(t-0.09,2)
            else:
                styles.append({
                        'if': {
                            'filter_query':'{{{col}}} >= {mix} && {{{col}}} < {max}'.format( col=col, mix=num, max=num+x/20),
                            'column_id':col
                        },
                        'backgroundColor':'rgba(244, 67, 54   ,{})'.format(t),
                        'border': '0px solid rgba(244, 67, 54   ,{})'.format(t),
                        'color':'MidnightBlue'
                    })
                t = round(t+0.09,2)
            num -= x/20
    styles.append({'if': {'state': 'active'},'backgroundColor': 'rgba(0, 116, 217, 0.3)','border': '0px solid rgb(0, 116, 217)'})
    return styles

page = html.Div(
    [   
        dbc.ListGroupItem(
            [
                dbc.ListGroupItemHeading(html.H3('市场宽度')),
                dbc.ListGroupItemText(html.P('代表市场的涨跌的钟摆运动。当总数低于200-高于1000，进入极值区间。投资者在极值区操作最佳。')),
            ]
        ),
        html.Br(),
        dash_table.DataTable(
        id='martket-breadth',
        columns=([{'id': p,'name': col[p]} for p in df.columns]),
        data=df.to_dict('records'),
        style_header={'backgroundColor': 'gold','fontWeight': 'bold','textAlign': 'center','height': '60px','whiteSpace': 'normal',},
        style_table={'width': 'auto'},
        style_cell={'width': '55px','fontSize': 18,'textAlign': 'center','height': '40px'},
        style_data_conditional=table_style(df),
        )

    ],
    className="container",)
