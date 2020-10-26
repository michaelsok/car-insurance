import json
import requests

from flask import jsonify


class API(object):
    HEADERS = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

    def __init__(self, url='http://0.0.0.0:8080', route='api'):
        self.url = url
        self.route = route

    @property
    def api_route(self):
        return f'{self.url}/{self.route}/'

    def post(self, inputs):
        values = json.dumps(inputs)
        results = requests.post(self.api_route, data=values, headers=self.HEADERS)
        return json.loads(results.text)
