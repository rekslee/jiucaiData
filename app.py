# -*- coding: utf-8 -*-
import os, sys
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from apps import data_dict, macro_data, fed, panoramic,martket_breadth
from datas import date, symbol_data
from config.config import * 

path=os.path.abspath('.')   
sys.path.append(path)
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True,title='韭菜数据--美股市场宽度和全景图',update_title='耐心等待...')

navbar = dbc.NavbarSimple(
    children=[
        dcc.Interval(id="time-interval", n_intervals=1, interval=1000*60*60*1),
        dbc.NavItem(dbc.NavLink("宏观经济",href="/page-1",active=True,id="page-1-link")),
        dbc.NavItem(dbc.NavLink("联储数据", href="/page-2", id="page-2-link")),
        dbc.NavItem(dbc.NavLink("市场宽度", href="/page-3", id="page-3-link")),
        dbc.NavItem(dbc.NavLink("全景图", href="/page-4",id="page-4-link")),
        dbc.NavItem(dbc.NavLink("数据字典", href="/page-5", id="page-5-link")),
        dbc.NavItem(dbc.NavLink("机器荐股", href="/page-6", id="page-6-link", disabled=True)),
        dbc.NavItem(dbc.NavLink("投资计划", href="/page-7", id="page-7-link", disabled=True)),
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src='https://robotics.upc.edu/en/software/github-mark-light-32px-1.png', height="30px"), className="ml-5"),
                    dbc.Col(dbc.NavbarBrand("GitHub", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://github.com/rekslee/jiucaiData",
        ),

    ],brand="韭菜数据",brand_href="/",
    color="dark",
    fixed = 'top',
    dark=True,
)
jumbotron = dbc.Jumbotron(
    [
        dbc.Container(
            [   
                html.H1("韭菜数据Dash", className="display-5"),
                html.P("数据源来自Fred&Yahoo Finance,更新时间:-,-,-",className="lead",id='update-time'),
                html.P("未来会添加自动荐股器和交易计划等",className="lead",),
            ],fluid=True,
        )
    ],fluid=True,)
app.layout = html.Div(children=[
    navbar,
    html.Br(),
    dbc.Spinner(html.Div(id="loading-output"),color="primary",size="lg",fullscreen=True),
    html.Div(children=[dcc.Location(id="url"),html.Div(id="page-content")],className="container-fluid"),
    jumbotron,
],id='serve-layout',className = 'p-5')

# 定时更新数据库
@app.callback(Output("update-time", "children"),Input("time-interval", "n_intervals"))
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

app.scripts.config.serve_locally = True
server = app.server
# app.layout = serve_layout()

if __name__ == '__main__':
    app.run_server(debug=True)