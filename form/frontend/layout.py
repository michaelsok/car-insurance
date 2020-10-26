import dash_core_components as dcc
import dash_html_components as html

import form.frontend.sidebar.layout as sidebar
import form.frontend.contents.layout as contents


def _get_layout(logo='grey_logo.png'):
    layout = html.Div(children=[
        dcc.Location(id="url"),
        sidebar._get_layout(logo=logo),
        contents._get_layout()
        ])
    return layout
