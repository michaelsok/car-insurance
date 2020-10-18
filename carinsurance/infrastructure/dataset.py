import os
import re
import json
import logging
import zipfile

from kaggle.api.kaggle_api_extended import KaggleApi


class CarInsuranceDataset(object):
    PATH = 'kondla/carinsurance'

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger()
        self.api = KaggleApi()
        self.api.authenticate()

    @property
    def zipname(self):
        return f'{os.path.basename(self.PATH)}.zip'

    def download(self, filepath=None):
        self.logger.info(f'Downloading kaggle dataset from {self.PATH}')
        self.api.dataset_download_files(self.PATH, path=filepath)

    def unzip(self, filepath, dirpath=None, delete=True):
        dirpath = dirpath or os.path.abspath(os.path.dirname(filepath))
        self.logger.info(f'Unzipping file {filepath}')
        with zipfile.ZipFile(filepath, 'r') as f:
            f.extractall(dirpath)

        if delete:
            self.logger.info(f'Removing file {filepath}')
            os.remove(filepath)

    def rename_files_in(self, dirpath):
        self.logger.info(f'Reading files in {dirpath}')
        files = os.listdir(dirpath)

        for f in files:
            for dataset in ('train', 'test'):
                if re.match(f'.*_{dataset}.csv', f) is not None:
                    self.logger.info(f'Renaming file {f} into {dataset}.csv')
                    os.rename(os.path.join(dirpath, f), os.path.join(dirpath, f'{dataset}.csv'))
