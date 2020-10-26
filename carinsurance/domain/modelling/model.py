import os
import pickle

from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report


class Model(object):
    '''Model class for fitting a scikit-learn model,
    computing performances and saving both model and results

    Parameters
    ----------
    name : str, optional, default is "RandomForest"
        name of scikit-learn model to use
        must be either "RandomForest", "LogisticRegression", "DecisionTree" or "GradientBoosting"
    results_path : str or NoneType, optional, default is None
        path where results and performances will be saved,
        if None the results won't be saved
    **modelargs
        keyword arguments to use in scikit-learn model initialization

    Attributes
    ----------
    name : str
        name of scikit-learn model to use
    results_path : str or NoneType
        path where results and performances will be saved,
        if None the results won't be saved
    model : scikit-learn classifier model
        model use to fit the data among the ones accepted:
        - DecisionTreeClassifier
        - RandomForestClassifier
        - LogisticRegression
        - GradientBoostingClassifier

    '''
    MODELS = {
        'RandomForest': RandomForestClassifier,
        'LogisticRegression': LogisticRegression,
        'DecisionTree': DecisionTreeClassifier,
        'GradientBoosting': GradientBoostingClassifier,
    }

    def __init__(self, name='RandomForest', results_path=None, **modelargs):
        assert name in self.MODELS.keys()
        self.name = name
        self.results_path = results_path
        self.model = self.MODELS[name](**modelargs)

    def train(self, data, target, **fitargs):
        '''Fit the data with the model

        Parameters
        ----------
        data : array-like of shape (n_samples, n_features)
            training data for fitting the model
        target : array-like of shape (n_samples,)
            training target for fitting the model
        **fitargs
            keyword argument for the fit method of model

        '''
        self.model.fit(data, target, **fitargs)

    def predict(self, data, **predictargs):
        '''Predict the probabilities on the given data
        through predict_proba (when available) or predict method

        Parameters
        ----------
        data : array-like of shape (n_samples, n_features)
            data on which probabilities must be computed

        Returns
        -------
        array-like of shape (n_samples, n_classes)
            probabilities computed for every class

        '''
        if hasattr(self.model, 'predict_proba'):
            return self.model.predict_proba(data, **predictargs)
        return self.model.predict(data, **predictargs)

    def compute_report_using(self, data, target, threshold=.5, name='report.txt'):
        '''Compute classification report based on data, target and the given threshold,
        if results_path was not initialized with None, also save it

        Parameters
        ----------
        data : array-like of shape (n_samples, n_features)
            data used to compute the classification report
        target : array-like of shape (n_samples,)
            target used to compute the classification report
        threshold : float, optional, default is .5
            threshold used for splitting the class, must be between 0 and 1
        name : str, optional, default is "report.txt"
            name of the classification report file when saved,
            only used if results path is not set to None

        Returns
        -------
        str
            classification report computed with data, target and given threshold

        '''
        assert (threshold >= 0) and (threshold <= 1)
        predictions = (self.predict(data)[:, 1] > threshold).astype(int)
        report = classification_report(target, predictions)

        if self.results_path is not None:
            with open(os.path.join(self.results_path, name), 'w') as f:
                f.write(report)

        return report

    def save(self, models_path, model_name=None):
        '''Save the model to given path with pickle dump method

        Parameters
        ----------
        models_path : str
            directory path where the model will be saved
        model_name : str or NoneType, optional, default is None
            filename used for saving the model, if None use name attribute
            followed by ".pkl" extension

        '''
        model_name = model_name or f'{self.name}.pkl'
        with open(os.path.join(models_path, model_name), 'wb') as f:
            pickle.dump(self.model, f)

    def load(self, model_path):
        '''Load the model from a given filepath with pickle load method. 

        Parameters
        ----------
        model_path : str
            filepath where the given model is storaged

        '''
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        name = type(model).__name__.replace('Classifier', '')
        assert name in self.MODELS.keys()
        self.model, self.name = model, name
