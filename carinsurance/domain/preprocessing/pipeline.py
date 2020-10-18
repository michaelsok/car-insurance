import pandas as pd
from sklearn.pipeline import Pipeline

from carinsurance.domain.preprocessing.transformers import DurationTransformer, Scaler
from carinsurance.infrastructure.preprocessing.transformers import (ColumnsRemover, NullValuesFiller,
    ModalitiesReplacement, DatetimeConverter, Dummifier, Indexer, ColumnsSorter
)


JOB_REPLACEMENT = {
    'admin.': 'administrative',
    'services': 'administrative',
    'self-employed': 'entrepreneur'
}

EDUCATION_REPLACEMENT = {
    'primary': 1,
    'secondary': 2,
    'tertiary': 3
}

CATEGORICAL_FEATURES = ['Job', 'Marital', 'Communication', 'Outcome']


def get_pipeline():
    pipeline = Pipeline([
        ('IdIndexer', Indexer(column='Id')),
        ('NullValuesFiller', NullValuesFiller(columns=['Communication', 'Outcome'], value='unknown')),
        ('JobAggregator', ModalitiesReplacement(column='Job', replacement=JOB_REPLACEMENT)),
        ('EducationEncoding', ModalitiesReplacement(column='Education', replacement=EDUCATION_REPLACEMENT)),
        ('DatetimeConverter', DatetimeConverter(columns=['CallStart', 'CallEnd'])),
        ('CallDuration', DurationTransformer(start='CallStart', end='CallEnd')),
        ('TimeColumnsRemover', ColumnsRemover(columns=['CallStart', 'CallEnd', 'LastContactMonth', 'LastContactDay'])),
        ('Dummifier', Dummifier(categoricals=CATEGORICAL_FEATURES)),
        ('ColumnsSorter', ColumnsSorter()),
        ('StandardScaler', Scaler(name='standard'))
    ])
    return pipeline
