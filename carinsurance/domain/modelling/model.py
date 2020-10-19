import os
import pickle
import logging

from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report


MODELS = {
    'RandomForest': RandomForestClassifier,
    'LogisticRegression': LogisticRegression,
    'DecisionTree': DecisionTreeClassifier,
    'GradientBoosting': GradientBoostingClassifier,
}


class Model(object):
    def __init__(self, name='RandomForest', results_path=None, logger=None, **modelargs):
        assert name in MODELS.keys()
        self.name = name
        self.results_path = results_path
        self.logger = logging.getLogger()
        self.model = MODELS[name](**modelargs)

    def train(self, features, target, **fitargs):
        self.model.fit(features, target, **fitargs)

    def predict(self, features, **predictargs):
        if hasattr(self.model, 'predict_proba'):
            return self.model.predict_proba(features, **predictargs)
        return self.model.predict(features, **predictargs)

    def compute_report_using(self, features, target, threshold=.5, name=None):
        name = name or 'report.txt'
        predictions = (self.predict(features)[:, 1] > threshold).astype(int)
        report = classification_report(target, predictions)

        self.logger.info(report)
        if self.results_path is not None:
            with open(os.path.join(self.results_path, name), 'w') as f:
                f.write(report)

    def save(self, models_path, name=None):
        model_name = name or 'model.pkl'

        with open(os.path.join(models_path, model_name), 'wb') as f:
            pickle.dump(self.model, f)

    def load(self, model):
        self.model = model
        self.name = model.__name__.replace('Classifier', '')
