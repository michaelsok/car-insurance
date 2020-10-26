import os
import json

import numpy as np
import pandas as pd

from carinsurance import logger
from carinsurance.config import CONFIG


def _get_dataset_from(raw_path, logger):
    dataset = pd.read_csv(os.path.join(raw_path, 'test.csv'))
    dataset.drop('CarInsurance', axis=1, inplace=True) # remove target
    dataset.fillna('', inplace=True) # remove non-serializable values
    return dataset


def _create_batch_example_from(dataset, integers, floats):
    example = dataset.to_dict(orient='list')

    for column, values in example.items():
        if column in integers:
            example[column] = [int(value) for value in values]
        elif column in floats:
            example[column] = [float(value) for value in values]

    return example


def _create_online_examples_from(dataset, integers, floats):
    examples = dataset.to_dict(orient='records')

    for example in examples:
        for column, value in example.items():
            if column in integers:
                example[column] = [int(value)]
            elif column in floats:
                example[column] = [float(value)]

    return examples


def create_test_examples_from(config, logger):
    raw_path = os.path.join(config['project'], config['data'], 'raw')
    examples_path = os.path.join(config['project'], config['data'], 'examples')
    batch_path = os.path.join(examples_path, 'batch')
    online_path = os.path.join(examples_path, 'online')

    identifier_column = 'Id'
    integers = [
        'Id', 'Age', 'Default', 'Balance', 'HHInsurance', 'CarLoan',
        'LastContactDay', 'NoOfContacts', 'DaysPassed', 'PrevAttempts'
    ]
    floats = []

    if not os.path.exists(batch_path):
        logger.info('Create batch directory...')
        os.makedirs(batch_path, exist_ok=True)

    if not os.path.exists(online_path):
        logger.info('Create online directory...')
        os.makedirs(online_path, exist_ok=True)

    logger.info('Get test dataset...')
    dataset = _get_dataset_from(raw_path, logger)
    logger.info('Create batch example...')
    batch = _create_batch_example_from(dataset, integers=integers, floats=floats)
    logger.info('Create online examples...')
    onlines = _create_online_examples_from(dataset, integers=integers, floats=floats)

    logger.info('Save batch example...')
    with open(os.path.join(batch_path, 'batch.json'), 'w') as f:
        json.dump(batch, f, indent=4)

    logger.info('Save online examples...')
    for online in onlines:
        identifier = online[identifier_column][0]
        logger.debug(f'Save online {identifier} example...')
        with open(os.path.join(online_path, f'online_{identifier}.json'), 'w') as f:
            json.dump(online, f, indent=4)


if __name__ == '__main__':
    create_test_examples_from(CONFIG, logger)
