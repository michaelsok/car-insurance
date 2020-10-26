import dash_html_components as html
import dash_bootstrap_components as dbc


def _get_layout(logo='grey_logo.png'):
    layout = dbc.Row(children=[
        dbc.Col(html.Center(html.Img(src=f'assets/{logo}', width='100%', className='display-4'))),
        dbc.Col(children=[
            html.Button(
                # use the Bootstrap navbar-toggler classes to style
                html.Span(className='navbar-toggler-icon'),
                className='navbar-toggler',
                # the navbar-toggler classes don't set color
                style={
                    'color': 'rgba(255,255,255,.5)',
                    'border-color': 'rgba(255,255,255,.1)',
                    'background-color': 'rgba(255,255,255,.1)'
                },
                id='navbar-toggle'
            ),
            html.Button(
                # use the Bootstrap navbar-toggler classes to style
                html.Span(className='navbar-toggler-icon'),
                className='navbar-toggler',
                # the navbar-toggler classes don't set color
                style={
                    'color': 'rgba(255,255,255,.5)',
                    'border-color': 'rgba(255,255,255,.1)',
                    'background-color': 'rgba(255,255,255,.1)'
                },
                id='sidebar-toggle')
            ],
            # the column containing the toggle will be only as wide as the
            # toggle, resulting in the toggle being right aligned
            width='auto',
            # vertically align the toggle in the center
            align='center'
            ),
        ]
    )
    return layout
