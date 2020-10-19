'''Transformers with no business knowledge'''

import pandas as pd

from carinsurance.helpers.preprocessing import Transformer


class Indexer(Transformer):
    '''Transformer which uses a column as index

    Parameters
    ----------
    column : str
        column to transform as index

    Attributes
    ----------
    column : str
        column to transform as index

    '''
    def __init__(self, column):
        self.column = column

    def transform(self, data):
        '''Use the column set during initialization as index for given data

        Parameters
        ----------
        data : pd.DataFrame
            data for which index must be set

        Returns
        -------
        pd.DataFrame
            data with column set as index

        '''
        data = data.copy()
        data.set_index(self.column, inplace=True)
        return data


class DatetimeConverter(Transformer):
    '''Transformer which converts datetime-like columns encoded as string into true datetime format

    Parameters
    ----------
    columns : list-like
        columns to convert into datetime

    Attributes
    ----------
    columns : list-like
        columns to convert into datetime

    '''
    def __init__(self, columns):
        self.columns = columns

    def transform(self, data):
        '''Convert the columns set during initialization as datetime format for given data

        Parameters
        ----------
        data : pd.DataFrame
            data with columns to convert as datetime format

        Returns
        -------
        pd.DataFrame
            data with columns converted to datetime format

        '''
        data = data.copy()
        for column in self.columns:
            data[column] = pd.to_datetime(data[column])
        return data


class ModalitiesReplacement(Transformer):
    '''Transformer which replaces modalities present in column

    Parameters
    ----------
    column : str
        column on which modalities must be replaced
    replacement : dict, optional, default is dict()
        replacement pattern where keys are original modalities and
        value is replacement

    Attributes
    ----------
    column : str
        column on which modalities must be replaced
    replacement : dict, optional, default is dict()
        replacement pattern where keys are original modalities and
        value is replacement

    '''
    def __init__(self, column, replacement=dict()):
        self.column = column
        self.replacement = replacement

    def transform(self, data):
        '''Replace modalities present in data column with replacement set during initialization

        Parameters
        ----------
        data : pd.DataFrame
            data for which modalities in column must be replaced

        Returns
        -------
        pd.DataFrame
            data with modalities replaced

        '''
        data = data.copy()
        data[self.column].replace(to_replace=self.replacement, inplace=True)
        return data


class Dummifier(Transformer):
    '''Transformer which encodes categorical columns in one-hot-encoding

    Parameters
    ----------
    categoricals : list-like of str
        categorical columns to dummify

    Attributes
    ----------
    categoricals : list-like of str
        categorical columns to dummify
    columns :  pd.Index
        columns present after dummification fitting

    '''
    def __init__(self, categoricals):
        self.categoricals = categoricals
        self.columns = None

    def fit(self, data, drop_last=True):
        '''Get dummies columns present

        Parameteters
        ------------
        data : pd.DataFrame
            data to dummify
        drop_last : bool, optional, default is True
            if True, drop rarest modality

        Returns
        -------
        self : object
            Dummifier instance fitted

        '''
        dummies = pd.get_dummies(data, columns=self.categoricals)

        if drop_last:
            for c in self.categoricals:
                last = data[c].value_counts().index.values[-1]
                dummies.drop(f'{c}_{last}', axis=1, inplace=True)

        self.columns = dummies.columns
        return self

    def transform(self, data):
        '''Dummify data based on modalities seen during fit

        Parameters
        ----------
        data : pd.DataFrame
            data to dummify

        Returns
        -------
        pd.DataFrame
            data dummified based on modalities seen during fitting

        '''
        data = data.copy()
        frame = pd.get_dummies(data, columns=self.categoricals)
        return frame.reindex(columns=self.columns, fill_value=0)


class NullValuesFiller(Transformer):
    '''Transformer which replaces null values by given value

    Parameters
    ----------
    columns : list-like of str
        columns on which null values will be replaced
    value : any, optional, default is 0
        value used in place of null values

    Attributes
    ----------
    columns : list-like of str
        columns on which null values will be replaced
    value : any, optional, default is 0
        value used in place of null values

    '''
    def __init__(self, columns, value=0):
        self.columns = columns
        self.value = value

    def transform(self, data):
        '''Fill null values with value set during initialization

        Parameters
        ----------
        data : pd.DataFrame
            data for which null values in columns will be replaced by value

        Returns
        -------
        pd.DataFrame
            data with null values in columns replaced by value

        '''
        data = data.copy()
        for column in self.columns:
            data[column].fillna(self.value, inplace=True)
        return data


class ColumnsRemover(Transformer):
    '''Transformer which removes columns

    Parameters
    ----------
    columns : list-like of str
        columns to remove

    Attributes
    ----------
    columns : list-like of str
        columns to remove

    '''
    def __init__(self, columns):
        self.columns = columns

    def transform(self, data):
        '''Remove columns in data

        Parameters
        ----------
        data : pd.DataFrame
            data for which columns will be dropped

        Returns
        -------
        pd.DataFrame
            data with columns dropped

        '''
        data = data.copy()
        return data.drop(self.columns, axis=1)


class ColumnsSorter(Transformer):
    '''Transformer which sorts columns

    Attributes
    ----------
    columns : list-like of str
        columns sorted during fitting

    '''
    def __init__(self):
        self.columns = None

    def fit(self, data, y=None):
        '''Get columns order from data

        Parameters
        ----------
        data : pd.DataFrame
            data for which columns order will be memorized
        y : any, optional, default is None
            argument used for compatibility after TargetSplitter, ignored

        Returns
        -------
        self : object
            ColumnsSorter instance fitted

        '''
        self.columns = data.columns
        return self

    def transform(self, data, y=None):
        '''Sort data based on columns order during fitting

        Parameters
        ----------
        data : pd.DataFrame
            data for which columns muste be sorted
        y : any, optional, default is None
            argument used for compatibility after TargetSplitter, ignored

        Returns
        -------
        pd.DataFrame, any
            data with columns sorted and second argument

        '''
        data = data.copy()

        if y is None:
            return data[self.columns]
        return data[self.columns], y
