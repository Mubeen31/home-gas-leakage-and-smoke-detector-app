import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import dash_daq as daq
import pyrebase
from data import config

firebase = pyrebase.initialize_app(config)
db = firebase.database()

metaTags = [
    {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minium-scale=0.5'}]

app = dash.Dash(__name__, meta_tags=metaTags)
server = app.server

app.layout = html.Div([

    html.Div([
        html.Div([
            html.Div([
                html.Img(src=app.get_asset_url('leakage.png'),
                         className='image'),
                html.Div('IOT Gas Leakage and Smoke Detector',
                         style={'line-height': '15px'},
                         className='title_text')
            ], className='title_row')
        ], className='title_background twelve columns')
    ], className='row'),

    dcc.Interval(id='blink_image',
                 interval=1 * 3000,
                 n_intervals=0),

    html.Div([
        html.Div([

            html.Div([
                html.Div(id='temp_value'),
                html.Div([
                    dbc.Spinner(html.Div(id='sound_image')),
                    html.Div(id='black_sound_image'),
                    daq.BooleanSwitch(id='alarm_button',
                                      on=True,
                                      color="#9B51E0",
                                      ),
                    html.Div([
                        html.P('Select value for alarm', style={'color': '#666666'}),
                        dcc.Input(id='input_value_here',
                                  type='number',
                                  value=22,
                                  style={'margin-top': '-10px'}),
                    ], className='input_column')
                ], className='alarm_button_column')
            ], className='sound_image_row'),

            html.Div(id='alarm'),

        ], className='temp_container twelve columns')
    ], className='row'),

    html.Div([
        html.Div([

            html.Div([
                html.Div(id='gas_smoke_value'),
                html.Div([
                    dbc.Spinner(html.Div(id='gas_sound_image')),
                    html.Div(id='gas_black_sound_image'),
                    daq.BooleanSwitch(id='gas_alarm_button',
                                      on=True,
                                      color="#9B51E0",
                                      ),
                    html.Div([
                        html.P('Select value for alarm', style={'color': '#666666'}),
                        dcc.Input(id='input_value_here1',
                                  type='number',
                                  value=250,
                                  style={'margin-top': '-10px'}),
                    ], className='input_column'),
                ], className='alarm_button_column')
            ], className='sound_image_row'),

            html.Div(id='gas_alarm'),
        ], className='temp_container1 twelve columns')
    ], className='row'),

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
              [Input('blink_image', 'n_intervals')],
              [Input('alarm_button', 'on')],
              [State('input_value_here', 'value')]
              )
def update_value(n_intervals, button, input_value_here):
    temp_value = db.child('DHT').get('temperature')
    for item in temp_value.each():
        temp = item.val()

    if temp >= input_value_here and button == True:
        return [
            html.Audio(src=app.get_asset_url('alarm.mp3'),
                       autoPlay='AUTOPLAY',
                       controls=True,
                       loop='LOOP',
                       preload='yes',
                       style={'display': 'None'})
        ]
    elif temp >= input_value_here and button == False:
        return None
    elif temp < input_value_here:
        return None


@app.callback(Output('sound_image', 'children'),
              [Input('blink_image', 'n_intervals')],
              [Input('alarm_button', 'on')],
              [State('input_value_here', 'value')]
              )
def update_value(n_intervals, button, input_value_here):
    temp_value = db.child('DHT').get('temperature')
    for item in temp_value.each():
        temp = item.val()

    if temp >= input_value_here and button == True:
        return [
            html.Img(src=app.get_asset_url('alarm.png'))
        ]
    elif temp >= input_value_here and button == False:
        return None
    elif temp < input_value_here:
        return None


@app.callback(Output('black_sound_image', 'children'),
              [Input('blink_image', 'n_intervals')],
              [Input('alarm_button', 'on')],
              [State('input_value_here', 'value')]
              )
def update_value(n_intervals, button, input_value_here):
    temp_value = db.child('DHT').get('temperature')
    for item in temp_value.each():
        temp = item.val()

    if temp >= input_value_here and button == True:
        return None
    elif temp >= input_value_here and button == False:
        return [
            html.Img(src=app.get_asset_url('bell.png'))
        ]
    elif temp < input_value_here and button == False:
        return [
            html.Img(src=app.get_asset_url('bell.png'))
        ]
    elif temp < input_value_here and button == True:
        return [
            html.Img(src=app.get_asset_url('bell.png'))
        ]


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


@app.callback(Output('gas_alarm', 'children'),
              [Input('blink_image', 'n_intervals')],
              [Input('gas_alarm_button', 'on')],
              [State('input_value_here1', 'value')])
def update_value(n_intervals, button, input_value_here1):
    gas_value = db.child('MQ135').get('gas')
    for item in gas_value.each():
        gas = item.val()

    if gas >= input_value_here1 and button == True:
        return [
            html.Audio(src=app.get_asset_url('alarm.mp3'),
                       autoPlay='AUTOPLAY',
                       controls=True,
                       loop='LOOP',
                       preload='yes',
                       style={'display': 'None'})
        ]
    elif gas >= input_value_here1 and button == False:
        return None
    elif gas < input_value_here1:
        return None


@app.callback(Output('gas_sound_image', 'children'),
              [Input('blink_image', 'n_intervals')],
              [Input('gas_alarm_button', 'on')],
              [State('input_value_here1', 'value')])
def update_value(n_intervals, button, input_value_here1):
    gas_value = db.child('MQ135').get('gas')
    for item in gas_value.each():
        gas = item.val()

    if gas >= input_value_here1 and button == True:
        return [
            html.Img(src=app.get_asset_url('alarm.png'))
        ]
    elif gas >= input_value_here1 and button == False:
        return None
    elif gas < input_value_here1:
        return None


@app.callback(Output('gas_black_sound_image', 'children'),
              [Input('blink_image', 'n_intervals')],
              [Input('gas_alarm_button', 'on')],
              [State('input_value_here1', 'value')])
def update_value(n_intervals, button, input_value_here1):
    gas_value = db.child('MQ135').get('gas')
    for item in gas_value.each():
        gas = item.val()

    if gas >= input_value_here1 and button == True:
        return None
    elif gas >= input_value_here1 and button == False:
        return [
            html.Img(src=app.get_asset_url('bell.png'))
        ]
    elif gas < input_value_here1 and button == False:
        return [
            html.Img(src=app.get_asset_url('bell.png'))
        ]
    elif gas < input_value_here1 and button == True:
        return [
            html.Img(src=app.get_asset_url('bell.png'))
        ]


if __name__ == '__main__':
    app.run_server(debug=True)
