'''Transformers using business knowledge'''

import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from carinsurance.helpers.preprocessing import Transformer


class DurationTransformer(Transformer):
    '''Transformer which computes duration between datetime columns

    Parameters
    ----------
    start : str
        start column name
    end : str
        end column name
    column : str, optional, default is "duration"
        column name used for duration
    representation : str, optional, default is "minute"
        representation used for duration, should be either "second", "minute" or "hour"
    rounding : bool, optional, default is True
        if true, rounds up the duration

    Attributes
    ----------
    start : str
        start column name
    end : str
        end column name
    column : str
        column name used for duration
    representation : str
        representation used for duration, should be either "second", "minute" or "hour"
    rounding : bool, optional, default is True
        if true, rounds up the duration

    '''
    REPRESENTATIONS = ('second', 'minute', 'hour')
    def __init__(self, start, end, column='duration', representation='minute', rounding=True):
        assert representation in self.REPRESENTATIONS
        self.start = start
        self.end = end
        self.column = column
        self.representation = representation
        self.rounding = rounding

    def transform(self, data):
        '''Creates duration between start and end

        Parameters
        ----------
        data : pd.DataFrame
            data for which start and end will be used to compute duration

        Returns
        -------
        pd.DataFrame
            data with duration computed

        '''
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
    '''Transformer which splits a column from a dataset

    Parameters
    ----------
    column : str
        target column to split

    Attributes
    ----------
    column : str
        target column to split

    '''
    def __init__(self, column):
        self.column = column

    def transform(self, data):
        '''Splits target from data

        Parameters
        ----------
        data : pd.DataFrame
            data from which target must be splitted

        Returns
        -------
        pd.DataFrame, pd.Series
            pair of dataframe without target and target series

        '''
        data = data.copy()
        target = data.pop(self.column)
        return data, target


class Scaler(Transformer):
    '''Transformer which scales data based on overall values

    Parameters
    ----------
    name : str, optional, default is "standard"
        scaler name to use for fitting, must be either "standard" or "minmax"
    **scalerargs
        keyword arguments for scaler

    Attributes
    ----------
    name : str, optional, default is "standard"
        scaler name to use for fitting, must be either "standard" or "minmax"
    scaler : sklearn.preprocessing.StandardScaler or MinMaxScaler
        scaler to use for fitting

    '''

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
        '''Get scaling attributes from data

        Parameters
        ----------
        data : pd.DataFrame
            data to use for getting scaling attributes

        Returns
        -------
        object
            Scaler instance fitted

        '''
        data = data.copy()
        self.scaler.fit(data)
        return self

    def transform(self, data):
        '''Scales data based on fitting attributes

        Parameters
        ----------
        data : pd.DataFrame
            data to scale

        Returns
        -------
        pd.DataFrame
            data scaled with scaler

        '''
        data = data.copy()
        values = self.scaler.transform(data)
        return pd.DataFrame(values, columns=data.columns, index=data.index)


class MedianImputer(Transformer):
    '''Transformer which imputes data using median

    Parameters
    ----------
    columns : list-like of str
        columns for which null values will be imputed by median

    Attributes
    ----------
    columns : list-like of str
        columns for which null values will be imputed by median
    medians : dict
        medians found during fitting for imputation where keys are columns 
        and values are medians

    '''
    def __init__(self, columns):
        self.columns = columns
        self.medians = None

    def fit(self, data):
        '''Get medians from data columns

        Parameters
        ----------
        data : pd.DataFrame
            data used to compute medians for imputation

        Returns
        -------
        object
            MedianImputer instance fitted

        '''
        data = data.copy()
        self.medians = {c: data[c].median().astype(int) for c in self.columns}
        return self

    def transform(self, data):
        '''Imputes medians on null values in data columns

        Parameters
        ----------
        data : pd.DataFrame
            data for which null values must be imputed by medians

        Returns
        -------
        pd.DataFrame
            data with null values on columns replaced by medians

        '''
        data = data.copy()
        data.fillna(self.medians, inplace=True)
        return data
