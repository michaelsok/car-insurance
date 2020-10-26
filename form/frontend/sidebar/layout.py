import dash_html_components as html

import form.frontend.sidebar.side.layout as side
import form.frontend.sidebar.header.layout as header


def _get_layout(logo='grey_logo.png'):
    layout = html.Div(children=[
        header._get_layout(logo=logo),
        side._get_layout()
    ], id='sidebar')
    return layout
