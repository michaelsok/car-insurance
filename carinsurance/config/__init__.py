import os
import json


def _populate_environment(keypath):
    with open(keypath, 'r') as f:
        kaggle_json = json.load(f)
    os.environ['KAGGLE_USERNAME'] = kaggle_json['username']
    os.environ['KAGGLE_KEY'] = kaggle_json['key']


thispath = os.path.abspath(os.path.dirname(__file__))
environment = os.environ.get('CARINSURANCE_ENVIRONMENT')

filename = 'config.json'
if environment is not None:
    filename = f'config_{environment}.json'
filepath = os.path.join(thispath, filename)

with open(filepath, 'r') as f:
    CONFIG = json.load(f)

if CONFIG.get('keyname') is not None:
    CONFIG['keypath'] = os.path.join(thispath, CONFIG.get('keyname'))
    _populate_environment(CONFIG['keypath'])

project_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
CONFIG['project'] = CONFIG['project'] or project_path
