import dash

metaTags = [
    {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minium-scale=0.5'}]

app = dash.Dash(__name__, meta_tags=metaTags,
                suppress_callback_exceptions=True)
server = app.server
