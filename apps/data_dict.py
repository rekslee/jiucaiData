# -*- coding: utf-8 -*-
import dash_html_components as html
import dash_bootstrap_components as dbc
import os
import pandas as pd

path=os.path.abspath('.')
dict_data = pd.read_csv(path + "/config/financial_data_dict.csv")
page = html.Div([
    dbc.Table.from_dataframe(dict_data, striped=True, bordered=True, hover=True,dark=True),
    html.Br(),
],className="container")

