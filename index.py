import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import dash_daq as daq
import pyrebase
from data import config
from drop_down_list_values import temp_drop_down_list_values
from drop_down_list_values import gas_smoke_drop_down_list_values
from push_bullet import api_key
from pushbullet import Pushbullet

firebase = pyrebase.initialize_app(config)
db = firebase.database()

p_b = Pushbullet(api_key)

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
                        dcc.Dropdown(id='select_temp_value',
                                     multi=False,
                                     clearable=True,
                                     disabled=False,
                                     style={'display': True, 'margin-top': '-5px'},
                                     value=22,
                                     placeholder='Select Value',
                                     options=temp_drop_down_list_values),
                    ], className='drop_down_list_column')
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
                        dcc.Dropdown(id='select_gas_smoke_value',
                                     multi=False,
                                     clearable=True,
                                     disabled=False,
                                     style={'display': True, 'margin-top': '-5px'},
                                     value=210,
                                     placeholder='Select Value',
                                     options=gas_smoke_drop_down_list_values),
                    ], className='drop_down_list_column'),
                ], className='alarm_button_column')
            ], className='sound_image_row'),

            html.Div(id='gas_alarm'),
        ], className='temp_container twelve columns')
    ], className='row'),

    html.Div([
        html.Div([
            html.Div(id='temp_value1'),

            html.Div([
                html.Div([
                    html.Div(id='title'),
                    daq.BooleanSwitch(id='notifications',
                                      on=True,
                                      color="#9B51E0",
                                      ),
                ], className='notifications_row'),

                html.Div([
                    html.P('Select notification value for Temperature', style={'color': '#666666'}),
                    dcc.Dropdown(id='select_temp_value1',
                                 multi=False,
                                 clearable=True,
                                 disabled=False,
                                 style={'display': True, 'margin-top': '-5px'},
                                 value=22,
                                 placeholder='Select Value',
                                 options=temp_drop_down_list_values),
                ], className='drop_down_list_column')
            ], className='put_in_column')

        ], className='temp_container1 twelve columns')
    ], className='row'),

    html.Div([
        html.Div([
            html.Div(id='gas_smoke_value1'),

            html.Div([
                html.Div([
                    html.Div(id='title1'),
                    daq.BooleanSwitch(id='notifications1',
                                      on=True,
                                      color="#9B51E0",
                                      ),
                ], className='notifications_row'),

                html.Div([
                    html.P('Select notification value for gases and smoke', style={'color': '#666666'}),
                    dcc.Dropdown(id='select_temp_value2',
                                 multi=False,
                                 clearable=True,
                                 disabled=False,
                                 style={'display': True, 'margin-top': '-5px'},
                                 value=230,
                                 placeholder='Select Value',
                                 options=gas_smoke_drop_down_list_values),
                ], className='drop_down_list_column')
            ], className='put_in_column')

        ], className='temp_container2 twelve columns')
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
              [Input('select_temp_value', 'value')])
def update_value(n_intervals, button, select_temp_value):
    temp_value = db.child('DHT').get('temperature')
    for item in temp_value.each():
        temp = item.val()

    if temp >= select_temp_value and button == True:
        return [
            html.Audio(src=app.get_asset_url('alarm.mp3'),
                       autoPlay='AUTOPLAY',
                       controls=True,
                       loop='LOOP',
                       preload='yes',
                       style={'display': 'None'})
        ]
    elif temp >= select_temp_value and button == False:
        return None
    elif temp < select_temp_value:
        return None


@app.callback(Output('sound_image', 'children'),
              [Input('blink_image', 'n_intervals')],
              [Input('alarm_button', 'on')],
              [Input('select_temp_value', 'value')])
def update_value(n_intervals, button, select_temp_value):
    temp_value = db.child('DHT').get('temperature')
    for item in temp_value.each():
        temp = item.val()

    if temp >= select_temp_value and button == True:
        return [
            html.Img(src=app.get_asset_url('alarm.png'))
        ]
    elif temp >= select_temp_value and button == False:
        return None
    elif temp < select_temp_value:
        return None


@app.callback(Output('black_sound_image', 'children'),
              [Input('blink_image', 'n_intervals')],
              [Input('alarm_button', 'on')],
              [Input('select_temp_value', 'value')])
def update_value(n_intervals, button, select_temp_value):
    temp_value = db.child('DHT').get('temperature')
    for item in temp_value.each():
        temp = item.val()

    if temp >= select_temp_value and button == True:
        return None
    elif temp >= select_temp_value and button == False:
        return [
            html.Img(src=app.get_asset_url('bell.png'))
        ]
    elif temp < select_temp_value and button == False:
        return [
            html.Img(src=app.get_asset_url('bell.png'))
        ]
    elif temp < select_temp_value and button == True:
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
              [Input('select_gas_smoke_value', 'value')])
def update_value(n_intervals, button, select_gas_smoke_value):
    gas_value = db.child('MQ135').get('gas')
    for item in gas_value.each():
        gas = item.val()

    if gas >= select_gas_smoke_value and button == True:
        return [
            html.Audio(src=app.get_asset_url('alarm.mp3'),
                       autoPlay='AUTOPLAY',
                       controls=True,
                       loop='LOOP',
                       preload='yes',
                       style={'display': 'None'})
        ]
    elif gas >= select_gas_smoke_value and button == False:
        return None
    elif gas < select_gas_smoke_value:
        return None


@app.callback(Output('gas_sound_image', 'children'),
              [Input('blink_image', 'n_intervals')],
              [Input('gas_alarm_button', 'on')],
              [Input('select_gas_smoke_value', 'value')])
def update_value(n_intervals, button, select_gas_smoke_value):
    gas_value = db.child('MQ135').get('gas')
    for item in gas_value.each():
        gas = item.val()

    if gas >= select_gas_smoke_value and button == True:
        return [
            html.Img(src=app.get_asset_url('alarm.png'))
        ]
    elif gas >= select_gas_smoke_value and button == False:
        return None
    elif gas < select_gas_smoke_value:
        return None


@app.callback(Output('gas_black_sound_image', 'children'),
              [Input('blink_image', 'n_intervals')],
              [Input('gas_alarm_button', 'on')],
              [Input('select_gas_smoke_value', 'value')])
def update_value(n_intervals, button, select_gas_smoke_value):
    gas_value = db.child('MQ135').get('gas')
    for item in gas_value.each():
        gas = item.val()

    if gas >= select_gas_smoke_value and button == True:
        return None
    elif gas >= select_gas_smoke_value and button == False:
        return [
            html.Img(src=app.get_asset_url('bell.png'))
        ]
    elif gas < select_gas_smoke_value and button == False:
        return [
            html.Img(src=app.get_asset_url('bell.png'))
        ]
    elif gas < select_gas_smoke_value and button == True:
        return [
            html.Img(src=app.get_asset_url('bell.png'))
        ]


@app.callback(Output('title', 'children'),
              [Input('notifications', 'on')])
def update_value(push):
    if push == True:
        return [
            html.Div('Notifications are enabled')
        ]
    elif push == False:
        return [
            html.Div('Notifications are disabled')
        ]


@app.callback(Output('temp_value1', 'children'),
              [Input('blink_image', 'n_intervals')],
              [Input('notifications', 'on')],
              [Input('select_temp_value1', 'value')])
def update_value(n_intervals, push, value):
    temp_value = db.child('DHT').get('temperature')
    for item in temp_value.each():
        temp = item.val()

    if temp >= value and push == True:
        temp_noti = p_b.push_note(title='Warning!',
                                  body='Kitchen Temperature is increased.')
        return [
            html.Div(temp_noti),
        ]
    elif temp >= value and push == False:
        return None
    elif temp < value and push == True:
        return None
    elif temp < value and push == False:
        return None


@app.callback(Output('title1', 'children'),
              [Input('notifications1', 'on')])
def update_value(push):
    if push == True:
        return [
            html.Div('Notifications are enabled')
        ]
    elif push == False:
        return [
            html.Div('Notifications are disabled')
        ]


@app.callback(Output('gas_smoke_value1', 'children'),
              [Input('blink_image', 'n_intervals')],
              [Input('notifications1', 'on')],
              [Input('select_temp_value2', 'value')])
def update_value(n_intervals, push, value):
    gas_value = db.child('MQ135').get('gas')
    for item in gas_value.each():
        gas = item.val()

    if gas >= value and push == True:
        gas_noti = p_b.push_note(title='Warning!',
                                 body='Gases or smoke level is increased in kitchen.')
        return [
            html.Div(gas_noti),
        ]
    elif gas >= value and push == False:
        return None
    elif gas < value and push == True:
        return None
    elif gas < value and push == False:
        return None


if __name__ == '__main__':
    app.run_server(debug=True)
