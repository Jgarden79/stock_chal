import datetime
import dash
import dash_table
from dash_table import FormatTemplate
import numpy as np
import pandas as pd
from dash import html as html
import dash_bootstrap_components as dbc
from dash import dcc as dcc
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])
server = app.server
app.layout = html.Div([
    # First row
    dbc.Row([
        # logo here
        html.Img(src="https://jgarden79.github.io/PM_vis/lp_title.PNG",
                 style={'height': "25%", "width": "100%", 'display': 'block', 'margin-left': '0',
                        'margin-center': 'auto', "padding-bottom": "10px"})]),
    dbc.Row([
        html.Img(src="https://jgarden79.github.io/PM_vis/dollar.png",
                 style={'height': "1%", "width": "45%", 'display': 'block', 'margin-left': '27%',
                        'margin-center': 'auto', "padding-bottom": "10px"})]),

    dbc.Row([
        html.Div(id='league')]),
    dbc.Row([
        dbc.Col([html.Div(id = 'port')], width=4),
        dbc.Col(dcc.Graph(id = 'perf'), width=8)
    ])

])

if __name__ == '__main__':
    app.run_server(debug=True)


