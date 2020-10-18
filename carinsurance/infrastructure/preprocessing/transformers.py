import pandas as pd

from carinsurance.helpers.preprocessing import Transformer


class Indexer(Transformer):
    def __init__(self, column):
        self.column = column

    def transform(self, data):
        data = data.copy()
        data.set_index(self.column)
        return data


class DatetimeConverter(Transformer):
    def __init__(self, columns):
        self.columns = columns

    def transform(self, data):
        data = data.copy()
        for column in self.columns:
            data[column] = pd.to_datetime(data[column])
        return data


class ModalitiesReplacement(Transformer):
    def __init__(self, column, replacement=dict()):
        self.column = column
        self.replacement = replacement

    def transform(self, data):
        data = data.copy()
        data[self.column].replace(to_replace=self.replacement, inplace=True)
        return data


class Dummifier(Transformer):
    def __init__(self, categoricals):
        self.categoricals = categoricals
        self.columns = None

    def fit(self, data, drop_last=True):
        dummies = pd.get_dummies(data, columns=self.categoricals)

        if drop_last:
            for c in self.categoricals:
                last = data[c].value_counts().index.values[-1]
                dummies.drop(f'{c}_{last}', axis=1, inplace=True)

        self.columns = dummies.columns
        return self

    def transform(self, data):
        data = data.copy()
        frame = pd.get_dummies(data, columns=self.categoricals)
        return frame.reindex(columns=self.columns, fill_value=0)


class NullValuesFiller(Transformer):
    def __init__(self, columns, value=0):
        self.columns = columns
        self.value = value

    def transform(self, data):
        data = data.copy()
        for column in self.columns:
            data[column].fillna(self.value, inplace=True)
        return data


class ColumnsRemover(Transformer):
    def __init__(self, columns):
        self.columns = columns

    def transform(self, data):
        data = data.copy()
        return data.drop(self.columns, axis=1)


class ColumnsSorter(Transformer):
    def __init__(self):
        self.columns = None

    def fit(self, data, y=None):
        self.columns = data.columns
        return self

    def transform(self, data, y=None):
        data = data.copy()

        if y is None:
            return data[self.columns]
        return data[self.columns], y
