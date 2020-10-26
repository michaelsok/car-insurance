from datetime import date, datetime

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

JOB_OPTIONS = [
    dict(label='Manager', value='management'),
    dict(label='Ouvrier', value='blue-collar'),
    dict(label='Technicien', value='technician'),
    dict(label='Administratif', value='admin.'),
    dict(label='Service', value='services'),
    dict(label='Retraité', value='retired'),
    dict(label='Auto-Entrepreneur', value='self-employed'),
    dict(label='Sans Emploi', value='unemployed'),
    dict(label='Entrepreneur', value='entrepreneur'),
    dict(label='Étudiant', value='student'),
    dict(label='Au foyer', value='housemaid')
]

MARITAL_OPTIONS = [
    dict(label='Célibataire', value='single'),
    dict(label='Marié', value='married'),
    dict(label='Divorcé', value='divorced')
]

EDUCATION_OPTIONS = [
    dict(label='Primaire', value='primary'),
    dict(label='Secondaire', value='secondary'),
    dict(label='Tertiaire', value='tertiary'),
    dict(label='Inconnu', value='')
]

BOOLEAN_OPTIONS = [
    dict(label='Non', value=0),
    dict(label='Oui', value=1)
]

COMMUNICATION_OPTIONS = [
    dict(label='Fixe', value='telephone'),
    dict(label='Portable', value='cellular'),
    dict(label='Inconnu', value='')
]

OUTCOME_OPTIONS = [
    dict(label='Succès', value='success'),
    dict(label='Échec', value='failure'),
    dict(label='Autre', value='other'),
    dict(label='Inconnu', value='')
]


def _get_layout():
    layout = html.Div(children=[
        html.Center(html.H1('Formulaire')),
        html.Strong("Identifiant du client :"),
        dbc.Row(children=[
            dbc.Col(dcc.Input(id="id", type='number'), width=3),
            dbc.Col(width=6),
            dbc.Col(html.Button('Prédiction', id='post', n_clicks=0), width=3)
        ]),
        html.Br(),

        html.Strong("Age du client :"),
        dbc.Row(children=[
            dbc.Col(
                dcc.Slider(id="age", min=18, max=100, step=1, value=40, tooltip=dict(always_visible=True, placement='bottom'),
                marks={
                    18: '18',
                    25: '25',
                    30: '30',
                    40: '40',
                    50: '50',
                    60: '60',
                    70: '70',
                    80: '80',
                    90: '90',
                    100: '100'
                }
                )),
        ]),
        html.Br(),

        dbc.Row(children=[
            dbc.Col(children=[
                html.Strong("Métier du client :"),
                dcc.Dropdown(id='job', options=JOB_OPTIONS, value='management')
                ]),
            dbc.Col(children=[
                html.Strong("Situation maritale du client :"),
                dcc.Dropdown(id='marital', options=MARITAL_OPTIONS, value='single')
                ]),
            dbc.Col(children=[
                html.Strong("Niveau d'éducation du client :"),
                dcc.Dropdown(id='education', options=EDUCATION_OPTIONS, value='tertiary')
                ]),
        ]),
        html.Br(),

        dbc.Row(children=[
            dbc.Col(children=[
                html.Strong("En défaut :"),
                dcc.Dropdown(id='default', options=BOOLEAN_OPTIONS, value=0),
                ]),
            dbc.Col(children=[
                html.Strong("Solde annuel moyen (en $) :"),
                dcc.Input(id="balance", type='number', placeholder='Balance', value=0),
                ]),
            dbc.Col(children=[
                html.Strong("Assurance habitation :"),
                dcc.Dropdown(id='hh_insurance', options=BOOLEAN_OPTIONS, value=0),
                ]),
            dbc.Col(children=[
                html.Strong("Prêt automobile :"),
                dcc.Dropdown(id='car_loan', options=BOOLEAN_OPTIONS, value=0),
                ]),
                
        ]),
        html.Br(),

        dbc.Row(children=[
            dbc.Col(children=[
                dbc.Row(dbc.Col(html.Strong("Date du dernier contact :"))),
                dbc.Row(dbc.Col(
                        dcc.DatePickerSingle(id='last_contact',
                        min_date_allowed=date(2017, 1, 1),
                        max_date_allowed=date(2030, 12, 31),
                        initial_visible_month=datetime.today().date(),
                        date=datetime.today().date()
                    )
                ))
            ]),
            dbc.Col(children=[
                html.Strong("Moyen de communication utilisé :"),
                dcc.Dropdown(id='communication', options=COMMUNICATION_OPTIONS, value='cellular')
            ])
        ]),
        html.Br(),

        dbc.Row(children=[
            dbc.Col(children=[
                html.Strong("Heure de début d'appel"),
                dbc.Row(children=[
                    dbc.Col(dcc.Input(id="start_hour", type='number', placeholder='Heure', value=14), width=4),
                    dbc.Col(dcc.Input(id="start_minutes", type='number', placeholder='Minutes', value=0), width=4),
                    dbc.Col(dcc.Input(id="start_seconds", type='number', placeholder='Secondes', value=0), width=4),
                ])
            ], width=6),
            dbc.Col(children=[
                html.Strong("Heure de fin d'appel"),
                dbc.Row(children=[
                    dbc.Col(dcc.Input(id="end_hour", type='number', placeholder='Heure', value=14), width=4),
                    dbc.Col(dcc.Input(id="end_minutes", type='number', placeholder='Minutes', value=5), width=4),
                    dbc.Col(dcc.Input(id="end_seconds", type='number', placeholder='Secondes', value=0), width=4),
                ])
            ], width=6)
        ]),
        html.Br(),

        dbc.Row(children=[
            dbc.Col(children=[
                dbc.Row(dbc.Col(html.Strong("Nombre de contacts durant cette campagne :"))),
                dbc.Row(dbc.Col(dcc.Input(id="nb_contacts", type='number', value=2)))
                ]),
            dbc.Col(children=[
                dbc.Row(dbc.Col(html.Strong("Nombre de contacts avant cette campagne :"))),
                dbc.Row(dbc.Col(dcc.Input(id="prev_attempts", type='number', value=2)))
                ]),
            dbc.Col(children=[
                dbc.Row(dbc.Col(html.Strong("Nombre de jours depuis la dernière campagne :"))),
                dbc.Row(dbc.Col(dcc.Input(id="days_passed", type='number', value=100)))
                ]),
            dbc.Col(children=[
                dbc.Row(dbc.Col(html.Strong("Résultat de la dernière campagne effectuée :"))),
                dbc.Row(dbc.Col(dcc.Dropdown(id='outcome', options=OUTCOME_OPTIONS, value='failure'))),
                ]),
        ]),
        html.Br(),

        dbc.Row(dbc.Col(children=[
            html.Center(
                html.P(children=[
                    html.Span(id='results')
                ])
            )
        ]))
    ])
    return layout
