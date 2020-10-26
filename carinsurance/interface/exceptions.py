'''Exceptions raised during the inference step in the API call'''


class MissingValueError(Exception):
    pass


class ReplaceEmptyByNullError(Exception):
    pass


class TransformPipelineError(Exception):
    pass


class PredictionError(Exception):
    pass


class FloatAlterationError(Exception):
    pass


class IntegerAlterationError(Exception):
    pass
