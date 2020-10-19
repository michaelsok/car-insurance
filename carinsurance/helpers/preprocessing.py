'''Helper classes and functions for preprocessing'''

from sklearn.base import BaseEstimator, TransformerMixin


class Transformer(BaseEstimator, TransformerMixin):
    '''Base class for transformers used in pipeline (add a default fit function)'''
    def fit(self, data, **fitargs):
        '''Method used for compatibility with sklearn.pipeline.Pipeline'''
        return self
