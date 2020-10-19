import os
import json
import requests

import numpy as np
import pandas as pd

from carinsurance.config import CONFIG


#URL = 'http://0.0.0.0:8080/api/'
URL = 'https://blog-msok-ml-290723.ew.r.appspot.com/api'

if __name__ == '__main__':
    test = pd.read_csv(os.path.join(CONFIG['project'], CONFIG['data'], 'raw', 'test.csv'))
    test = test.drop('CarInsurance', axis=1)
    test = test.fillna('')
    value = test.iloc[:10].to_dict(orient='list')
    integers = ['Id', 'Age', 'Default', 'Balance', 'HHInsurance', 'CarLoan', 'LastContactDay', 'NoOfContacts',
                'DaysPassed', 'PrevAttempts']

    for k, v in value.items():
        if k in integers:
            if not isinstance(v, list):
                value[k] = [int(v)]
            else:
                value[k] = [int(item) for item in v]
        else:
            if not isinstance(v, list):
                value[k] = [v]
            else:
                value[k] = v

    value = json.dumps(value)

    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.post(URL, data=value, headers=headers)
    print(json.loads(r.text))
