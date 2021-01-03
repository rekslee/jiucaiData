# -*- coding: utf-8 -*-
import os, sys
import dash_auth
path=os.path.abspath('.')   
sys.path.append(path)
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output,State
from apps import data_dict, macro_data, fed, panoramic,martket_breadth
import pandas as pd
from datas import date, symbol_data, sql_data
from config.config import * 
# from flask_caching import Cache
from flask import Flask
VALID_USERNAME_PASSWORD_PAIRS = [['reks', 'wind']]
server = Flask(__name__)
server.config.update(DEBUG=True)  
server.debug=True
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP], 
    suppress_callback_exceptions=True,
    server=server,
    url_base_pathname="/")
auth = dash_auth.BasicAuth(app,VALID_USERNAME_PASSWORD_PAIRS)
app.scripts.config.serve_locally = True
app.debug=True
# cache = Cache(app.server, config={
#     'CACHE_TYPE': 'filesystem',
#     'CACHE_DIR': 'cache-directory'
# })
navbar = dbc.NavbarSimple(
    children=[
        dcc.Interval(id="time-interval", n_intervals=0, interval=1000*60*60*6),
        dbc.NavItem(dbc.NavLink("宏观经济",href="/page-1",active=True,id="page-1-link")),
        dbc.NavItem(dbc.NavLink("联储数据", href="/page-2", id="page-2-link")),
        dbc.NavItem(dbc.NavLink("市场宽度", href="/page-3", id="page-3-link")),
        dbc.NavItem(dbc.NavLink("全景图", href="/page-4",id="page-4-link")),
        dbc.NavItem(dbc.NavLink("数据字典", href="/page-5", id="page-5-link")),
        dbc.NavItem(dbc.NavLink("机器荐股", href="/page-6", id="page-6-link", disabled=True)),
        dbc.NavItem(dbc.NavLink("投资计划", href="/page-7", id="page-7-link", disabled=True)),
        # dbc.Button("刷新数据", color="warning", className="mr-1",id='load-btn'),
    ],brand="韭菜数据",brand_href="/",
    color="dark",
    # sticky="top",
    fixed = 'top',
    dark=True,
)
jumbotron = dbc.Jumbotron(
    [
        dbc.Container(
            [   
                html.H1("金融数据Dash", className="display-5"),
                html.P("数据源来自Fred&Yahoo Finance,更新时间:-,-,-",className="lead",id='update-time'),
                html.P("未来会添加自动荐股器和交易计划等",className="lead",),
            ],fluid=True,
        )
    ],fluid=True,)
def serve_layout():
    return html.Div(children=[
    navbar,
    html.Br(),
    dbc.Spinner(html.Div(id="loading-output")),
    html.Div(children=[dcc.Location(id="url"),html.Div(id="page-content")],className="container-fluid"),
    jumbotron,
    
],id='serve-layout',className = 'p-5')
app.layout = serve_layout()

# 定时更新数据库
@app.callback(Output("update-time", "children"),Input("time-interval", "n_intervals"),prevent_initial_call=True)
def update_progress(n):
    symbol_data.update_data()
    return '数据源来自Fred&Yahoo Finance,更新时间:{}'.format(date.now())

# 初始化页面
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 6)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        return True, False, False, False, False
    return [pathname == f"/page-{i}" for i in range(1, 6)]


# 更新页面
@app.callback([Output('page-content', 'children'),Output("loading-output", "children")], Input('url', 'pathname'),)
def display_page(pathname):
    if pathname in ['/', '/page-1']:
        return macro_data.page, ''
    elif pathname == '/page-2':
        return fed.page, ''
    elif pathname == '/page-3':
        return martket_breadth.page, ''
    elif pathname == '/page-4':
        return panoramic.page, ''
    elif pathname == '/page-5':
        return data_dict.page, ''
    return dbc.Jumbotron([html.H1("404: Not found", className="text-danger"),html.Hr()]), ''



# 储存数据字典
@app.callback(
    Output('dict-store', 'data'),
    Input('dict-table', 'data_timestamp'),
    State('dict-table', 'data'),
    prevent_initial_call=True
    )
def update_dict_to_DB(data_timestamp,data):
    print('fix=================',data_timestamp)
    df = pd.DataFrame(data)
    db = '{}/datas/db/{}.db'.format(path, config.get('database', 'data_dict'))
    sql_data.dataToDB(db, df, config.get('tablename', 'data_dict'))
    return data

@app.callback(
    Output('dict-table', 'data'),
    Input('dict-store', 'data'),
    prevent_initial_call=True
    )
def get_dict_from_store(data):
    return data


@server.route("/")
def jiucai():
    return app.index()