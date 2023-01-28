from app import app
from dash import html
from dash import dcc
from dash.dependencies import Output, Input
import pandas as pd
import plotly.graph_objs as go
import pyrebase
from data import config

firebase = pyrebase.initialize_app(config)
db = firebase.database()

page_one_layout = html.Div([

    dcc.Interval(id='blink_image',
                 interval=1 * 3000,
                 n_intervals=0),

    html.Div([
        html.Div([
            html.Div(id='temp_value'),
            html.Div(id='alarm'),
        ], className='temp_container twelve columns')
    ], className='row'),

    html.Div([
        html.Div([
            html.Div(id='gas_smoke_value')
        ], className='temp_container twelve columns')
    ], className='row')

])


@app.callback(Output('temp_value', 'children'),
              [Input('blink_image', 'n_intervals')])
def update_value(n_intervals):
    temp_value = db.child('DHT').get('temperature')
    for item in temp_value.each():
        temp = item.val()

    return [
        html.Div([
            html.Div([
                html.Div('{0:.1f}'.format(temp),
                         className='numeric_value'),
                html.Div('°C', className='symbol')
            ], className='value_symbol'),

            html.Div([
                html.Img(src=app.get_asset_url('temp.png')),
                html.Div('Room Temperature', style={'color': '#666666'})
            ], className='image_text')
        ], className='value_image_text_column')
    ]


@app.callback(Output('alarm', 'children'),
              [Input('blink_image', 'n_intervals')])
def update_value(n_intervals):
    temp_value = db.child('DHT').get('temperature')
    for item in temp_value.each():
        temp = item.val()

    if temp >= 19.0:
        return [
            html.Audio(src=app.get_asset_url('alarm.mp3'),
                       autoPlay='AUTOPLAY',
                       controls=True,
                       loop='LOOP',
                       preload='yes',
                       style={'display': 'None'})
        ]
    elif temp < 19.0:
        return None


@app.callback(Output('gas_smoke_value', 'children'),
              [Input('blink_image', 'n_intervals')])
def update_value(n_intervals):
    gas_value = db.child('MQ135').get('gas')
    for item in gas_value.each():
        gas = item.val()

    return [
        html.Div([
            html.Div([
                html.Div('{0:.0f}'.format(gas),
                         className='numeric_value'),
                html.Div('Level', className='symbol')
            ], className='value_symbol'),

            html.Div([
                html.Img(src=app.get_asset_url('flames.png')),
                html.Div('Gases and Smoke', style={'color': '#666666'})
            ], className='image_text')
        ], className='value_image_text_column')
    ]
