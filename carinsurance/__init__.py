import os
import logging
from logging.handlers import RotatingFileHandler

from carinsurance.config import CONFIG

LOGS_DIR = os.path.join(CONFIG['project'], CONFIG['logs'])
LOGS_PATH = os.path.join(LOGS_DIR, 'logs.log')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)


# Don't create logs if no rights are given for writing
try:
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR, exist_ok=True)

    file_handler = RotatingFileHandler(os.path.join(LOGS_DIR, 'logs.log'))
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
except Exception as e:
    logger.info('Logs won\'t be saved on files')
