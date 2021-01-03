# -*- coding: utf-8 -*-
import dash_html_components as html
import dash_table
import datetime as dt
import dash_core_components as dcc
import os, sys
path=os.path.abspath('.')   
sys.path.append(path)
from datas import sql_data
from config.config import *

tablename = config.get('tablename','data_dict')
dictDB = '{}/datas/db/{}.db'.format(path, config.get('database','data_dict'))
df =sql_data.readDB(dictDB, tablename)

page = html.Div([
    dcc.Store(id='dict-store',storage_type='local'),
    dash_table.DataTable(
        id='dict-table',
        css=[{'selector': '.row','rule': 'margin: 0'}],
        columns=([{'id': p,'name': p} for p in df.columns.tolist()]),
        data=df.to_dict('records'),
        editable=True,
        style_header={
            'backgroundColor': 'gold',
            'height': '55px',
            'fontWeight': 'bold',
            'fontSize': 14,
            'textAlign': 'center',
        },
        # page_size=15,
        style_data={
            'whiteSpace': 'normal',
            'height': '55px',
            'fontSize': 12,
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            },
            {
                'if': {'state': 'active'},
                'backgroundColor': 'rgba(0, 116, 217, 0.3)',
                'border': '2px solid rgb(0, 116, 217)'
            },
            {
                'if': {'column_type':'text'},
                'textAlign': 'left'
            },
        ],
        style_cell_conditional=[
            {'if': {'column_id': 'Explanation'},'width': '250px',},
        ],
    ),
],className="container")

