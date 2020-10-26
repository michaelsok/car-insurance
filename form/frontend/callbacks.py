import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import form.frontend.sidebar as sidebar
import form.frontend.pages.form as form
import form.frontend.pages.introduction as introduction


def _get_callbacks_from(app, url='http://0.0.0.0:8080'):

    @app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
    def render_page_content(pathname):
        if pathname in ['/', '/introduction']:
            return introduction._get_layout()
        elif pathname in ['/form']:
            return form._get_layout()
        # If the user tries to reach a different page, return a 404 message
        return dbc.Jumbotron(
            [
                html.H1('404: Not found', className='text-danger'),
                html.Hr(),
                html.P(f"L'url {pathname} n\'est pas reconnue..."),
            ]
        )

    @app.callback(
        [Output('introduction-link', 'active'),
         Output('form-link', 'active')],
        [Input('url', 'pathname')]
    )
    def toggle_active_links(pathname):
        if pathname == '/':
            # Treat introduction as the homepage / index
            return True, False
        return [pathname == 'introduction-link', pathname == 'form-link']

    sidebar_callbacks = sidebar._get_callbacks_from(app)
    form_callbacks = form._get_callbacks_from(app, url=url)
    callbacks = (render_page_content, toggle_active_links) + sidebar_callbacks + form_callbacks

    return callbacks
