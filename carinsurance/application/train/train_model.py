import os
import pickle

import pandas as pd

from carinsurance import logger
from carinsurance.config import CONFIG
from carinsurance.domain.modelling.model import Model


def train_model(config, logger):
    clean_path = os.path.join(config['project'], config['data'], 'clean')
    models_path = os.path.join(config['project'], config['models'])
    results_path = os.path.join(config['project'], config['results'])

    if not os.path.exists(results_path):
        logger.info('Creating results_path directory...')
        os.makedirs(results_path, exist_ok=True)

    logger.info('Reading train dataset...')
    X_train = pd.read_csv(os.path.join(clean_path, 'train.csv'))
    y_train = pd.read_csv(os.path.join(clean_path, 'y_train.csv'))

    logger.info('Reading validation dataset...')
    X_validation = pd.read_csv(os.path.join(clean_path, 'validation.csv'))
    y_validation = pd.read_csv(os.path.join(clean_path, 'y_validation.csv'))

    logger.info('Creating model...')
    model = Model(name='RandomForest', results_path=results_path)
    logger.info('Training model...')
    model.train(X_train, y_train.values.reshape(-1))
    logger.info('Save report on validation...')
    model.compute_report_using(X_validation, y_validation.values.reshape(-1), threshold=.5)

    logger.info('Saving model...')
    model.save(os.path.join(models_path), model_name='model.pkl')

    logger.info('Model trained!')


if __name__ == '__main__':
    train_model(CONFIG, logger)
