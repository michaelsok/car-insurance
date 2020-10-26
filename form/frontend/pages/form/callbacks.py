from datetime import date

from dash.dependencies import Input, Output, State

from form.backend.api import API


MONTHS = {
        1: 'jan',
        2: 'feb',
        3: 'mar',
        4: 'apr',
        5: 'may',
        6: 'jun',
        7: 'jul',
        8: 'aug',
        9: 'sep',
        10: 'oct',
        11: 'nov',
        12: 'dec'
    }

MAPPING = dict(
    id='Id', age='Age', job='Job', marital='Marital', education='Education',
    default='Default', balance='Balance', hh_insurance='HHInsurance',
    car_loan='CarLoan', communication='Communication', last_contact='LastContact',
    start_hour='StartHour', start_minutes='StartMinutes', start_seconds='StartSeconds',
    end_hour='EndHour', end_minutes='EndMinutes', end_seconds='EndSeconds',
    nb_contacts='NoOfContacts', prev_attempts='PrevAttempts', days_passed='DaysPassed',
    outcome='Outcome'
)


def _get_callbacks_from(app, url='http://0.0.0.0:8080'):
    api = API(url=url)

    outputs = Output('results', 'children')
    inputs = [Input('post', 'n_clicks')]

    order, states = list(), list()
    for identifier in MAPPING.keys():
        states.append(State(identifier, 'value' if identifier != 'last_contact' else 'date'))
        order.append(identifier)

    @app.callback(outputs, inputs, states)
    def call_api(n_clicks, *api_inputs):
        if n_clicks == 0:
            return ''

        api_inputs = {MAPPING[key]: value for key, value in zip(order, [*api_inputs])}
        last_contact = api_inputs.pop('LastContact')
        last_contact = date.fromisoformat(last_contact)

        try:
            api_inputs['LastContactDay'] = last_contact.day
            api_inputs['LastContactMonth'] = MONTHS[last_contact.month]
        except AttributeError:
            return "La dernière date de contact n'est pas renseignée!"

        try:
            start = f"{api_inputs.pop('StartHour'):02}:{api_inputs.pop('StartMinutes'):02}:{api_inputs.pop('StartSeconds'):02}"
        except AttributeError:
            return "L'horaire de début d'appel n'est pas renseigné"

        try:
            end = f"{api_inputs.pop('EndHour'):02}:{api_inputs.pop('EndMinutes'):02}:{api_inputs.pop('EndSeconds'):02}"
        except AttributeError:
            return "L'horaire de fin d'appel n'est pas renseigné"

        api_inputs['CallStart'], api_inputs['CallEnd'] = start, end

        for key, value in api_inputs.items():
            api_inputs[key] = [value if value is not None else '']

        results = api.post(api_inputs)
        if results['status'] == 1:
            return "Une erreur est apparue durant l'inférence!"

        probability = results['probabilities'][0]
        return 'Le model a prédit avec un score de {:.2%}'.format(probability)

    return (call_api,)
