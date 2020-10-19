import os
import json
import pickle
import logging

import numpy as np
import pandas as pd
from flask import Flask, request, redirect, url_for, flash, jsonify

from carinsurance.config import CONFIG


def get_predictions(data, pipeline, model, threshold=.5):
    data.replace({'': np.nan}, inplace=True)
    values = pipeline.transform(data)
    probabilities = model.predict_proba(values)[:, 1]
    probabilities = [float(p) for p in probabilities]
    return probabilities


def get_answer_from(probabilities, threshold=.5, message=None):
    status = int(probabilities is None)
    predictions = None
    if probabilities is not None:
        predictions = [int(p > threshold) for p in probabilities]

    answer = {
        'status': status,
        'message': message,
        'predictions': predictions,
        'probabilities': probabilities
    }
    return answer


def get_app_from(name, pipeline, model, threshold=.5, logger=None):
    app = Flask(name)
    logger = logger or logging.getLogger()

    @app.route('/api/', methods=['POST'])
    def predict():
        try:
            data = request.get_json()
        except Exception as e:
            logger.error(str(e))
            return get_answer_from(probabilities=None, message='Data couldn\'t be parsed')

        try:
            data = pd.DataFrame(data)
        except Exception as e:
            logger.error(str(e))
            return get_answer_from(probabilities=None, message='Data couldn\'t be converted into a dataframe')

        try:
            probabilities = get_predictions(data, pipeline, model)
        except Exception as e:
            return get_answer_from(probabilities=None, message='No predictions could be computed')

        return get_answer_from(probabilities=probabilities)

    return app
