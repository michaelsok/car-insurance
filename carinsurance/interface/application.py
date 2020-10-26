'''Functions used to create the Flask App served by the gunicorn command'''

import os
import json
import pickle
import logging

import numpy as np
import pandas as pd
from flask import Flask, request
from werkzeug.exceptions import BadRequest

from carinsurance.interface.exceptions import (
    ReplaceEmptyByNullError, TransformPipelineError, PredictionError,
    FloatAlterationError, IntegerAlterationError
)


def get_predictions(data, pipeline, model, threshold, logger):
    '''Get predictions from data, a preprocessing pipeline, an inference model 
    and a threshold
    Since data is expected to have empty string to replace missing data, first step 
    is to replace empty string with NaN values

    Parameters
    ----------
    data : array-like of shape (n_samples, n_features)
        data for which we want inference
    pipeline : sklearn.pipeline.Pipeline
        preprocessing pipeline for ML tasks
    model : sklearn model API
        model use to compute probabilities
    threshold : float, optional, default is .5
        threshold for splitting classes
    logger : logging.Logger
        logger used to display inference errors

    Returns
    -------
    list of float
        probabilities for each instance present in data

    Raises
    ------
    ReplaceEmptyByNullError
        arises when an error occurs during empty string replacement
    TransformPipelineError
        arises when an error occurs during the pipeline transform step
    PredictionError
        arises when an error occurs during the prediction step
    FloatAlterationError
        arises when an error occurs during the transformation step of the 
        probabilities into float type for json serialization during request
    IntegerAlterationError
        arises when an error occurs during transformation from probabilities to predictions 

    '''
    try:
        data.replace({'': np.nan}, inplace=True)
    except Exception as e:
        logger.exception(str(e))
        message = "An error arised during replace method from data"
        raise ReplaceEmptyByNullError(message)
    try:
        values = pipeline.transform(data)
    except Exception as e:
        logger.exception(str(e))
        message = "An error arised during transform method from pipeline"
        raise TransformPipelineError(message)

    try:
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(values)[:, 1]
        else:
            probabilities = model.predict(values)
    except Exception as e:
        logger.exception(str(e))
        message = "An error arised during prediction from model"
        raise PredictionError(message)

    try:
        probabilities = [float(p) for p in probabilities]
    except Exception as e:
        logger.exception(str(e))
        message = "An error arised during float function on model prediction"
        raise FloatAlterationError(message)

    try:
        predictions = [int(p > threshold) for p in probabilities]
    except Exception as e:
        logger.exception(str(e))
        message = "An error arised during int function on probabilities"
        raise IntegerAlterationError(message)

    return probabilities, predictions


def get_answer_from(identifiers, probabilities, predictions=None, message=None):
    '''Get json answer to send through POST method after a call to the model API

    Parameters
    ----------
    identifiers : list of int
        identifiers from the probabilities
    probabilities : list of float or NoneType
        probabilities computed by the API
    predictions : list of int or NoneType, optional, default is None
        predictions associated with probabilities
    message : str or NoneType, optional, default is None
        message to return with the answer,
        it might be comments or error logging

    Returns
    -------
    dict
        json answer throught the API, with 4 components:
        - status: 0 if no error, 1 if there was one during call
        - message: comments or error logging
        - predictions: list of 0 and 1 meaning respectively 
          no subscribtion and subscription inferred
        - probabilities: associated probabilities to the decision

    '''
    status = int(probabilities is None)
    answer = {
        'identifiers': identifiers,
        'status': status,
        'message': message,
        'predictions': predictions,
        'probabilities': probabilities
    }
    return answer


def get_app_from(name, pipeline, model, threshold=.5, logger=None):
    '''Get Flask App with the api POST route used to infer predictions

    Parameters
    ----------
    name : str
        name of current process (should be __main__)
    pipeline : sklearn.pipeline.Pipeline
        pipeline used to preprocess data
    model : sklearn model API
        model use to compute probabilities
    threshold : float
        threshold used to change probabilities into predictions
    logger : logging.Logger or NoneType, optional, default is None
        logger used to log message, if None use default logging logger

    Returns
    -------
    flask.App
        flask API with POST route for inference

    '''
    app = Flask(name)
    logger = logger or logging.getLogger()
    expected_inference_exceptions = (
        ReplaceEmptyByNullError, TransformPipelineError, PredictionError, FloatAlterationError, IntegerAlterationError
    )

    @app.route('/api/', methods=['POST'])
    def predict():
        try:
            try:
                data = request.get_json()
            except BadRequest as e:
                logger.exception(str(e))
                message = "Data couldn't be parsed"
                return get_answer_from(identifiers=None, probabilities=None, message=message)
    
            try:
                identifiers = data['Id']
            except KeyError as e:
                logger.exception(str(e))
                message = "No identifiers were found"
                return get_answer_from(identifiers=None, probabilities=None, message=message)
        except Exception as e:
            logger.exception(str(e))
            message = "Unexpected exception?!"
            return get_answer_from(identifiers=None, probabilities=None, message=message)

        try:
            try:
                data = pd.DataFrame(data)
            except (ValueError, TypeError) as e:
                logger.exception(str(e))
                message = "Data couldn't be converted into a dataframe"
                return get_answer_from(identifiers=identifiers, probabilities=None, message=message)

            try:
                probabilities, predictions = get_predictions(data, pipeline, model, threshold=.5, logger=logger)
            except expected_inference_exceptions as e:
                logger.error(str(e))
                message = "No predictions could be computed"
                return get_answer_from(identifiers=identifiers, probabilities=None, message=message)
        except Exception as e:
            logger.exception(str(e))
            message = "Unexpected exception?!"
            return get_answer_from(identifiers=identifiers, probabilities=None, message=message)

        message = "Good answer"
        return get_answer_from(identifiers=identifiers, probabilities=probabilities, predictions=predictions, message=message)

    return app
