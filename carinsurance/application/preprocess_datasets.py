import os
import pickle

import pandas as pd
from sklearn.model_selection import train_test_split

from carinsurance import logger
from carinsurance.config import CONFIG
from carinsurance.domain.preprocessing.pipeline import get_pipeline


VALIDATION_SPLIT = .2


def preprocess_datasets(config, logger):
    raw_path = os.path.join(config['project'], config['data'], 'raw')
    clean_path = os.path.join(config['project'], config['data'], 'clean')
    models_path = os.path.join(config['project'], config['models'])

    if not os.path.exists(clean_path):
        logger.info('Creating clean directory...')
        os.makedirs(clean_path, exist_ok=True)

    if not os.path.exists(models_path):
        logger.info('Creating models directory...')
        os.makedirs(models_path, exist_ok=True)

    logger.info('Reading train dataset...')
    train = pd.read_csv(os.path.join(raw_path, 'train.csv'))
    logger.info('Splitting dataset into train and validation...')
    train, validation = train_test_split(train, test_size=VALIDATION_SPLIT)

    logger.info('Getting pipeline...')
    pipeline = get_pipeline()
    logger.info('Fitting pipeline on train...')
    train = pipeline.fit_transform(train)
    logger.info('Transforming validation with pipeline...')
    validation = pipeline.transform(validation)

    logger.info('Saving datasets...')
    train.to_csv(os.path.join(clean_path, 'train.csv'))
    validation.to_csv(os.path.join(clean_path, 'validation.csv'))
    logger.info('Saving pipeline...')
    with open(os.path.join(models_path, 'preprocessing_pipeline.pkl'), 'wb') as f:
        pickle.dump(pipeline, f)


if __name__ == '__main__':
    preprocess_datasets(CONFIG, logger)
