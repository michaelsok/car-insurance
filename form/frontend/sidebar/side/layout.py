import dash_html_components as html
import dash_bootstrap_components as dbc


def _get_layout():
    layout = dbc.Collapse(
        dbc.Nav(children=[
                    dbc.NavLink('Introduction', href='/introduction', id='introduction-link'),
                    dbc.NavLink('Formulaire', href='/form', id='form-link')
                ],
                vertical=True,
                pills=True,
                ),
            id='collapse',
        )
    return layout
