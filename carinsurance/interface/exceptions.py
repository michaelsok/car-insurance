'''Exceptions raised during the inference step in the API call'''

class ReplaceEmptyByNullError(Exception):
    'An error arised during replace method from data (pd.DataFrame expected)'


class TransformPipelineError(Exception):
    'An error arised during transform method from pipeline'


class PredictionError(Exception):
    'An error arised during prediction from model'


class FloatAlterationError(Exception):
    'An error arised during float function on model prediction'


class IntegerAlterationError(Exception):
    'An error arised during int function on probabilities'
