from dash import html
from dash import dcc
from dash.dependencies import Output, Input
import pandas as pd
import dash_bootstrap_components as dbc
from app import app
from tabContents.tab_one import page_one_layout
from tabContents.tab_two import page_two_layout
from tabContents.tab_three import page_three_layout
from tabContents.tab_four import page_four_layout

server = app.server

tab_style = {
    'border-top': 'none',
    'border-bottom': 'none',
    'border-left': 'none',
    'border-right': 'none',
    'backgroundColor': 'rgba(255, 255, 255, 0)',
    'height': '35px',
    'padding': '7.5px',
    'width': 'auto'
}

selected_tab_style = {
    'border-top': 'none',
    'border-bottom': '2px solid blue',
    'border-left': 'none',
    'border-right': 'none',
    'backgroundColor': 'rgba(255, 255, 255, 0)',
    'height': '35px',
    'padding': '7.5px',
    'width': 'auto'
}

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

    html.Div([
        html.Div([
            dcc.Tabs(id='tabs', value='content_tab_one', children=[
                dcc.Tab(label='Home',
                        value='content_tab_one',
                        style=tab_style,
                        selected_style=selected_tab_style),
                dcc.Tab(label='Setting',
                        value='content_tab_two',
                        style=tab_style,
                        selected_style=selected_tab_style),
                dcc.Tab(label='Alert',
                        value='content_tab_three',
                        style=tab_style,
                        selected_style=selected_tab_style),
                dcc.Tab(label='Activate',
                        value='content_tab_four',
                        style=tab_style,
                        selected_style=selected_tab_style)
            ], style={'display': 'flex', 'flex-direction': 'row'})
        ], className='tabs_container twelve columns')
    ], className='row'),

    html.Div(id='return_tab_content', children=[])

])


@app.callback(Output('return_tab_content', 'children'),
              [Input('tabs', 'value')])
def render_content(value):
    if value == 'content_tab_one':
        return page_one_layout
    elif value == 'content_tab_two':
        return page_two_layout
    elif value == 'content_tab_three':
        return page_three_layout
    elif value == 'content_tab_four':
        return page_four_layout


if __name__ == '__main__':
    app.run_server(debug=True)
