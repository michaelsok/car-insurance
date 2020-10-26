import os
import pickle

from carinsurance.config import CONFIG
from carinsurance.interface.application import get_app_from


MODEL_PATH = os.path.join(CONFIG['project'], CONFIG['models'], 'model.pkl')
PIPELINE_PATH = os.path.join(CONFIG['project'], CONFIG['models'], 'pipeline.pkl')

with open(MODEL_PATH, 'rb') as f:
    MODEL = pickle.load(f)

with open(PIPELINE_PATH, 'rb') as f:
    PIPELINE = pickle.load(f)

app = get_app_from(__name__, PIPELINE, MODEL)
