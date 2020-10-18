import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from carinsurance.helpers.preprocessing import Transformer


class DurationTransformer(Transformer):
    REPRESENTATIONS = ('second', 'minute', 'hour')
    def __init__(self, start, end, column='duration', representation='minute', rounding=True):
        assert representation in self.REPRESENTATIONS
        self.start = start
        self.end = end
        self.column = column
        self.representation = representation
        self.rounding = rounding

    def transform(self, data):
        data = data.copy()
        duration = (data[self.end] - data[self.start]).dt.seconds

        if self.representation == 'minute':
            duration /= 60
        elif self.representation == 'hour':
            duration /= 3600

        if self.rounding:
            data[self.column] = duration.round().astype(int)

        return data


class TargetSplitter(Transformer):
    def __init__(self, column):
        self.column = column

    def transform(self, data):
        data = data.copy()
        target = data.pop(self.column)
        return data, target


class Scaler(Transformer):
    SCALERS = ('standard', 'minmax')
    def __init__(self, name='standard', **scalerargs):
        assert name in self.SCALERS

        self.name = name
        if name == 'standard':
            self.scaler = StandardScaler(**scalerargs)
        elif name == 'minmax':
            self.scaler = MinMaxScaler(**scalerargs)
        else:
            raise ValueError(f'name should be in {self.SCALERS}')

    def fit(self, data):
        data = data.copy()
        self.scaler.fit(data)
        return self

    def transform(self, data):
        data = data.copy()
        values = self.scaler.transform(data)
        return pd.DataFrame(values, columns=data.columns, index=data.index)


class MedianImputer(Transformer):
    def __init__(self, columns):
        self.columns = columns
        self.medians = None

    def fit(self, data):
        data = data.copy()
        self.medians = {c: data[c].median().astype(int) for c in self.columns}
        return self

    def transform(self, data):
        data = data.copy()
        data.fillna(self.medians, inplace=True)
        return data
