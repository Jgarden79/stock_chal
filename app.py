import datetime
import dash
import dash_table
from dash_table import FormatTemplate
import pandas as pd
from dash import html as html
import dash_bootstrap_components as dbc
from dash import dcc as dcc
from dash.dependencies import Output, Input, State
import pandas_market_calendars as mcal
import plotly.graph_objects as go
import gspread


gc = gspread.oauth(credentials_filename="client_secret_279764153689-2rq7k9683jqc57dh9o6lf30jvatdec7m.apps.googleusercontent.com.json",)

# import league table:
today = datetime.datetime.today().date()
s_date = '2021-12-31'
nyse = mcal.get_calendar('NYSE') # set up calendar
market_days = nyse.valid_days(start_date=s_date, end_date=today).date
date = market_days[-2]
date = date.strftime("%Y-%m-%d")
sh = gc.open("league")
ws = sh.worksheet('league')
league_tab = pd.DataFrame(ws.get_all_records())
money = FormatTemplate.money(2)
percentage = FormatTemplate.percentage(2)

columns = [dict(name = league_tab.columns[0], id =league_tab.columns[0]),
           dict(name =league_tab.columns[1], id =league_tab.columns[1],type='numeric', format = percentage),
           dict(name =league_tab.columns[2], id =league_tab.columns[2],type='numeric', format = percentage),
           dict(name =league_tab.columns[3], id =league_tab.columns[3],type='numeric', format = percentage),
           dict(name =league_tab.columns[4], id =league_tab.columns[4],type='numeric', format = percentage),
           dict(name =league_tab.columns[5], id =league_tab.columns[5],type='numeric', format = percentage),
           dict(name =league_tab.columns[6], id =league_tab.columns[6]),
           dict(name =league_tab.columns[7], id =league_tab.columns[7],type='numeric', format = percentage),
           dict(name =league_tab.columns[8], id =league_tab.columns[8])]
data = league_tab.to_dict("records")

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
        dbc.Col([html.Img(src="https://jgarden79.github.io/PM_vis/MiLM4ebLT.gif",
                 style={'height': "125px", "width": "150px", 'display': 'block', 'margin-left': '50%',
                        'margin-center': 'auto', "padding-bottom": "10px"})],width=4),
        dbc.Col([html.Img(src="https://jgarden79.github.io/PM_vis/MiLM4ebLT.gif",
                          style={'height': "125px", "width": "150px", 'display': 'block', 'margin-left': '50%',
                                 'margin-center': 'auto', "padding-bottom": "10px"})], width=4),
        dbc.Col([html.Img(src="https://jgarden79.github.io/PM_vis/MiLM4ebLT.gif",
                          style={'height': "125px", "width": "150px", 'display': 'block', 'margin-left': '50%',
                                 'margin-center': 'auto', "padding-bottom": "10px"})], width=4),
    ]),

    dbc.Row([dash_table.DataTable(data = data, columns = columns,
                                  style_table = {'height':'485px', 'overflowY': 'auto'},
                                  fixed_rows={'headers': True},
                                  sort_mode='multi',
                                  sort_action='native',
                                  style_cell={'font_size': '14px'},
                                  style_data={
                                      'color': '#1F51FF',
                                      'backgroundColor': 'white',
                                      'fontWeight': 'bold',
                                      'opacity': '60%',
                                      'whiteSpace': 'normal',
                                      'height': 'auto',
                                      'lineHeight': '15px',
                                      "font-family": "sans-serif"},
                                  style_header={
                                      'backgroundColor': 'white',
                                      'color': '#1F51FF',
                                      'opacity': '60%',
                                      'fontWeight': 'bold',
                                      "font-family": "sans-serif"}
                                  )], style={'marginLeft': 'auto', 'marginRight': 'auto', "padding-bottom": "10px", "width":"95%"}),
    dbc.Row([
        dbc.Col([dcc.Dropdown(id="Player", options =[{"label":i,'value':i} for i in list(league_tab['Player'])],
                              value = list(league_tab['Player'])[0], style = {"width":"95%", 'marginLeft': 'auto', 'marginRight': 'auto'}),
                 html.Div(id = 'port',style = {'marginLeft': 'auto', 'marginRight': 'auto', "width":"95%"})],
                style = {'marginLeft': 'auto', 'marginRight': 'auto'}, width=4),
        dbc.Col(dcc.Graph(id = 'perf'), width=7, style = {'marginLeft': 'auto', 'marginRight': 'auto'})
    ])

], style={"background-image":"url(https://jgarden79.github.io/PM_vis/bg_page.GIF)",
          "background-repeat": "no-repeat", "background-size": "cover"})

@app.callback(Output('perf', "figure"),
              Input("Player", "value"))
def create_chrt(name):
    sh = gc.open("sc_perf")
    ws = sh.worksheet('{}_perf'.format(name))
    plot_df = pd.DataFrame(ws.get_all_records())
    #plot_df = pd.read_csv("assets/performance/{}_perf.csv".format(name), index_col=0)
    color_scheme = ['#0D1525', '#033C5A', '#339AC1', '#0482C3', '#00B04F', '#58595B', '#66A9CB', '#70AD45', '#FFCF31']
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=plot_df.index,
                             y=plot_df[plot_df.columns[2]],
                             line=dict(color=color_scheme[0]),
                             mode='lines',
                             name=name))

    fig.add_trace(go.Scatter(x=plot_df.index,
                             y=plot_df[plot_df.columns[5]],
                             line=dict(color=color_scheme[3]),
                             mode='lines',
                             name=plot_df.columns[5]))
    fig.update_layout(
        paper_bgcolor='rgba(255,255,255,0.5)',
        plot_bgcolor='rgba(255,255,255,0.5)',
        legend=dict(orientation="h"),
        yaxis_tickformat='.2%',
        yaxis_title="Total Return",
        font=dict(color='black'),
        hovermode="x unified",
        title=dict(text="<b>Performance {} vs {}</b>".format(name, plot_df.columns[5].split(" ")[0]),
                   font=dict(size=18, color='#FF10F0', ), x=0.5, y=0.95))
    return fig

@app.callback(Output("port", "children"),
             Input("Player", "value"))
def get_port(name):
    ### insert gsspred data
    sh = gc.open("sc_aps")
    ws = sh.worksheet('{}_apr'.format(name))
    port = pd.DataFrame(ws.get_all_records())
    port = pd.read_csv('assets/port_apps/{}_apr_{}.csv'.format(name, date))
    port = port.rename(columns={port.columns[0]: 'Ticker'})
    port['Shares'] = port['Shares'].round(2)
    columns = [dict(name = port.columns[0], id =port.columns[0]),
               dict(name =port.columns[1], id =port.columns[1]),
               dict(name =port.columns[2], id =port.columns[2],type='numeric', format = money),
               dict(name =port.columns[3], id =port.columns[3],type='numeric', format = money),
               dict(name =port.columns[4], id =port.columns[4],type='numeric', format = money),
               dict(name =port.columns[5], id =port.columns[5],type='numeric', format = percentage),
               dict(name =port.columns[6], id =port.columns[6],type='numeric', format = money)]
    data = port.to_dict("records")
    tab = dash_table.DataTable(data=data, columns=columns,
                         style_table={'height': '485px', 'overflowY': 'auto'},
                         fixed_rows={'headers': True},
                         sort_mode='multi',
                         sort_action='native',
                         style_cell={'font_size': '12px'},
                         style_data={
                             'color': '#B026FF',
                             'backgroundColor': 'white',
                             'whiteSpace': 'normal',
                             'opacity': '60%',
                             'height': 'auto',
                             'lineHeight': '15px',
                             'fontWeight': 'bold',
                             "font-family": "sans-serif"},
                         style_header={
                             'backgroundColor': 'white',
                             'color': 'black',
                             'opacity': '60%',
                             'fontWeight': 'bold',
                             "font-family": "sans-serif"}
                         )
    return tab


if __name__ == '__main__':
    app.run_server(debug=True)


