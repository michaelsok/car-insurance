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

try:
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR, exist_ok=True)

    file_handler = RotatingFileHandler(os.path.join(LOGS_DIR, 'logs.log'))
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
except (OSError, IOError, PermissionError): # Don't create logs if no rights are given for writing
    logger.info('Logs won\'t be saved on files due to permission errors')
except Exception as e:
    logger.error('Unexpected exception for logging rotating file handler')
    logger.error(str(e))
    raise e
