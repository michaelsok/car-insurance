import pandas as pd
from sklearn.pipeline import Pipeline

from carinsurance.domain.preprocessing.transformers import DurationTransformer, Scaler, MedianImputer
from carinsurance.infrastructure.preprocessing.transformers import (ColumnsRemover, NullValuesFiller,
    ModalitiesReplacement, DatetimeConverter, Dummifier, Indexer, ColumnsSorter
)


def get_pipeline():
    '''Get feature processing pipeline for ML tasks

    Returns
    -------
    sklearn.pipeline.Pipeline
        pipeline used to preprocess data before ML inference

    '''
    job_replacement = {'admin.': 'administrative', 'services': 'administrative', 'self-employed': 'entrepreneur'}
    education_replacement = {'primary': 1., 'secondary': 2., 'tertiary': 3.}
    categorical_features = ['Job', 'Marital', 'Communication', 'Outcome']

    pipeline = Pipeline([
        ('IdIndexer', Indexer(column='Id')),
        ('NullValuesFiller', NullValuesFiller(columns=['Communication', 'Outcome'], value='unknown')),
        ('JobAggregator', ModalitiesReplacement(column='Job', replacement=job_replacement)),
        ('EducationEncoding', ModalitiesReplacement(column='Education', replacement=education_replacement)),
        ('EducationImputer', MedianImputer(columns=['Education'])),
        ('DatetimeConverter', DatetimeConverter(columns=['CallStart', 'CallEnd'])),
        ('CallDuration', DurationTransformer(start='CallStart', end='CallEnd')),
        ('TimeColumnsRemover', ColumnsRemover(columns=['CallStart', 'CallEnd', 'LastContactMonth', 'LastContactDay'])),
        ('Dummifier', Dummifier(categoricals=categorical_features)),
        ('ColumnsSorter', ColumnsSorter()),
        ('StandardScaler', Scaler(name='standard'))
    ])
    return pipeline
