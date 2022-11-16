import dash
from dash import html, dcc
import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from interpret_serial import df, portList
from dash.dependencies import Input, Output, ClientsideFunction

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

# =====================================================================
# Gráficos

# graph_temperature = px.line(df, x="tempo", y=['temp_obj', 'temp_amb'], color='variable', title='Temperatura CVT' )
graph_temperature = go.Figure(layout={"template": "plotly_dark"})
graph_temperature.add_trace(
    go.Scatter(x=df["tempo"], y=df["temp_obj"], name="temp_obj", mode="lines", line=dict(color="#F6511D")))
graph_temperature.add_trace(
    go.Scatter(x=df["tempo"], y=df["temp_amb"], name="temp_amb", mode="lines", line=dict(color="#FFB400")))
graph_temperature.update_layout(yaxis_title="Temperatura CVT", margin=dict(l=5, r=5, t=5, b=5), autosize=True, height=150)

graph_velocidade = go.Figure(layout={"template": "plotly_dark"})
graph_velocidade.add_trace(
    go.Scatter(x=df["tempo"], y=df["VEL_D"], name="Roda Direita", mode="lines", line=dict(color="#F72585")))
graph_velocidade.add_trace(
    go.Scatter(x=df["tempo"], y=df["VEL_E"], name="Roda Esquerda", mode="lines", line=dict(color="#7209B7")))
graph_velocidade.update_layout(yaxis_title="Velocidade", margin=dict(l=5, r=5, t=5, b=5), autosize=True, height=150)

graph_PRM = go.Figure(layout={"template": "plotly_dark"})
graph_PRM.add_trace(
    go.Scatter(x=df["tempo"], y=df["RPM_motor"], name="Motor", mode="lines", line=dict(color="#26C485")))
graph_PRM.add_trace(go.Scatter(x=df["tempo"], y=df["RPM_roda"], name="Roda", mode="lines", line=dict(color="#A3E7FC")))
graph_PRM.update_layout(yaxis_title="Rotação", margin=dict(l=5, r=5, t=5, b=5), autosize=True, height=150)

graph_ACC = go.Figure(layout={"template": "plotly_dark"})
graph_ACC.add_trace(
    go.Scatter(x=df["tempo"], y=df["ACC"], name="acc (km/h²)", mode="lines", line=dict(color="#FF6F59")))
graph_ACC.update_layout(yaxis_title="Aceleração", margin=dict(l=5, r=5, t=5, b=5), autosize=True, height=150)

graph_laps = go.Figure(layout={"template": "plotly_dark"})
graph_laps.add_trace(go.Bar(x=df["tempo"], y=df["ACC"]))
graph_laps.update_layout(yaxis_title="Lap Times", margin=dict(l=5, r=5, t=5, b=5), autosize=True, height=170)

graph_map = go.Figure(layout={"template": "plotly_dark"})
graph_map.add_trace(
    go.Bar(x=df["tempo"], y=df["ACC"], name="acc (km/h²)"))
graph_map.update_layout(yaxis_title="Lap Time", margin=dict(l=5, r=5, t=5, b=5), autosize=True, height=150)
# =====================================================================
# Layout
app.layout = dbc.Container(children=[
    dbc.Row([
        dbc.Col([
            html.Div(children=[
                html.H5(children='BAJA UEA'),
                html.H6(children="Visualização dos dados da telemetria"),
            ]),
        ]),
        dbc.Col([
            dcc.Dropdown(['2400', '4800', '9600', '115200'], id='baudrate-dropdown', value='9600',
                         placeholder='Baudrate', style={'width': '150px'}),
            dcc.Dropdown(portList, id='ports-dropdown', value='portList[0]', placeholder='COM Ports',
                         style={'width': '150px'}),
            dbc.Button('Connect', id='connect-button', style={'width': '150px'}),
        ], class_name='d-flex p-3 align-items-center justify-content-evenly'),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='graph_temperature',
                figure=graph_temperature,
                className='h-20'
            ),
            dcc.Graph(
                id='graph_velocidade',
                figure=graph_velocidade
            ),
            dcc.Graph(
                id='graph_PRM',
                figure=graph_PRM
            ),
            dcc.Graph(
                id='graph_ACC',
                figure=graph_ACC
            ),
            dcc.Graph(
                id='graph_laps',
                figure=graph_laps,
            ),

        ], className="m-0 p-0 mh-100"),
        dbc.Col([
            dbc.Row([
                dbc.Col([dbc.Card([
                    dbc.CardBody([
                        html.H6("Velocidade", className="card-text text-center"),
                        html.H5("0", style={"color": "#EFE322", "text-align": "center"}, id="velocidade-text"),
                    ], className="m-0 p-0")
                ])], style={'padding-right': '0px'}, md=2),
                dbc.Col([dbc.Card([
                    dbc.CardBody([
                        html.H6("Rotação", className="card-text text-center"),
                        html.H5("0", style={"color": "#EFE322", "text-align": "center"}, id="rpm-text"),
                    ], className="m-0 p-0")
                ])], style={'padding-right': '0px'}, md=2),
                dbc.Col([dbc.Card([
                    dbc.CardBody([
                        html.H6("Aceleração", className="card-text text-center"),
                        html.H5("0", style={"color": "#EFE322", "text-align": "center"}, id="aceleração-text"),
                    ], className="m-0 p-0")
                ])], style={'padding-right': '0px'}, md=2),
                dbc.Col([dbc.Card([
                    dbc.CardBody([
                        html.H6("Distância", className="card-text text-center"),
                        html.H5("0", style={"color": "#EFE322", "text-align": "center"}, id="distancia-text"),
                    ], className="m-0 p-0")
                ])], style={'padding-right': '0px'}, md=2),
                dbc.Col([dbc.Card([
                    dbc.CardBody([
                        html.H6("Tanque", className="card-text text-center"),
                        html.H5("0", style={"color": "#EFE322", "text-align": "center"}, id="tanque-text"),
                    ], className="m-0 p-0")
                ])], style={'padding-right': '0px'}, md=2),
                dbc.Col([dbc.Card([
                    dbc.CardBody([
                        html.H6("Temperatura", className="card-text text-center"),
                        html.H5("0", style={"color": "#EFE322", "text-align": "center"}, id="tempo-text"),
                    ], className="m-0 p-0")
                ])], style={'padding-right': '0px'}, md=2)
            ], className="m-0 p-0 mh-100"),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            daq.Gauge(
                                color={"gradient": True,
                                       "ranges": {"#F6BDC0": [0, 25], "#F07470": [25, 50], "#DC1C13": [50, 80]}},
                                label='Velocidade',
                                id='gauge_velocidade',
                                value=6,
                                size=210,
                                max=80,
                                min=0,
                                style={'margin-top': '10px', 'padding-right': '0px'},
                                theme={
                                    'dark': True,
                                }
                            ),
                        ], md=6, class_name='m-auto'),
                        dbc.Col([
                            daq.Gauge(
                                color={"gradient": True, "ranges": {"#F6BDC0": [0, 2000], "#F07470": [2000, 4000],
                                                                    "#DC1C13": [4000, 6000]}},
                                label='Rotação',
                                size=210,
                                id='gauge_rpm',
                                value=3400,
                                max=6000,
                                min=0,
                                style={'margin-top': '10px'},
                                theme={
                                    'dark': True,
                                }
                            ),
                        ], md=6, class_name='m-auto'),

                    ], class_name='d-flex', style={'height': '250px'}),
                    dbc.Row([
                        daq.GraduatedBar(
                            color={"gradient": True, "ranges": {"red": [0, 2], "yellow": [2, 5], "green": [5, 10]}},
                            showCurrentValue=True,
                            value=10,
                            label='Bateria',
                            labelPosition='top',
                            theme={
                                'dark': True,
                            }
                        )
                    ], class_name='justify-content-center')
                ], md=8),

                dbc.Col([
                    daq.Thermometer(
                        value=35,
                        label='Temperatura CVT',
                        labelPosition='top',
                        min=0,
                        max=100,
                        height=230,
                        width=10,
                        style={'margin-top': '10px'},
                        color='#FF6C00',
                    )
                ], md=2, class_name='p-0'),

                dbc.Col([
                    daq.Tank(
                        id='tank',
                        value=5,
                        showCurrentValue=True,
                        units='litros',
                        min=0,
                        max=10,
                        height=250,
                        style={'margin-top': '10px'},
                        label='Nível do tanque',
                        labelPosition='top',
                        color='#00FFFF'
                    ),
                ], md=2)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.ListGroup([
                        dbc.ListGroupItem([
                            daq.LEDDisplay(
                                label="Tempo de volta",
                                value="1:34.421",
                                size=18,
                                labelPosition='top',
                                backgroundColor="#060606"
                            ),
                        ]),
                        dbc.ListGroupItem([
                            daq.LEDDisplay(
                                label="Velocidade Média",
                                value="55.42",
                                size=18,
                                labelPosition='top',
                                backgroundColor="#060606"
                            ),
                        ]),
                        dbc.ListGroupItem([
                            daq.LEDDisplay(
                                label="Aceleração Média",
                                value="23.92",
                                size=18,
                                labelPosition='top',
                                backgroundColor="#060606",
                            ),
                        ]),
                        dbc.ListGroupItem([
                            daq.LEDDisplay(
                                label="Distância Percorrida",
                                value="232.92",
                                size=18,
                                labelPosition='top',
                                backgroundColor="#060606",
                            ),
                        ]),

                    ], style={'margin': '8px', 'margin-bottom': '0px'}),
                ], md=3),
                dbc.Col([

                ])
            ])
        ], className="m-0 p-0 h-100")
    ], className="m-0 p-0")
], fluid=True, class_name="mh-100")

# =====================================================================
# Interactivity
if __name__ == '__main__':
    app.run_server()
