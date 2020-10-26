import dash_core_components as dcc
import dash_html_components as html


def _get_layout():
    layout = html.Div(children=[
        html.Center(html.H1('Introduction')),
        html.Br(),
        dcc.Markdown(
            """
            Cette application a pour objectif de montrer une manière simple de
            répondre à un problème de Machine Learning
            """
        )
    ])
    return layout
