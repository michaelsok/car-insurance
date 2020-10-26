import os

import dash
import dash_bootstrap_components as dbc

import form.frontend as frontend


gcp_project = os.environ.get('FORM_GCP_PROJECT')
url = 'http://0.0.0.0:8080' if gcp_project is None else f'https://{gcp_project}.ew.r.appspot.com'

app = dash.Dash(__name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
    suppress_callback_exceptions=True
)
server = app.server
app.layout = frontend._get_layout()
callbacks = frontend._get_callbacks_from(app, url=url)


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8090, debug=True)
