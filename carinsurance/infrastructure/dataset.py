'''Dataset for Cold Calls Insurance Dataset located at https://www.kaggle.com/kondla/carinsurance'''

import os
import re
import json
import logging
import zipfile

from kaggle.api.kaggle_api_extended import KaggleApi


class CarInsuranceDataset(object):
    '''Class to download Cold Calls Car Insurance Dataset
    available on Kaggle at https://www.kaggle.com/kondla/carinsurance
    using the Kaggle API

    Parameters
    ----------
    logger : logging.Logger or NoneType, optional, default is None
        logger to use for logging message,
        if None use logger with current logging config

    Attributes
    ----------
    logger : logging.Logger
        logger used for logging messages
    api : kaggle.api.kaggle_api_extended.KaggleApi
        kaggle API for authentication and downloading

    '''
    PATH = 'kondla/carinsurance'

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger()
        self.api = KaggleApi()
        self.api.authenticate()

    @property
    def zipname(self):
        '''Name used for zip file after download'''
        return f'{os.path.basename(self.PATH)}.zip'

    def download(self, dirpath=None):
        '''Download dataset into given directory path

        Parameters
        ----------
        dirpath : str or NoneType, optional, default is None
            directory path where dataset will be downloaded,
            if None download in current directory

        '''
        self.logger.info(f'Downloading kaggle dataset from {self.PATH}')
        self.api.dataset_download_files(self.PATH, path=dirpath)

    def unzip(self, filepath, dirpath=None, delete=True):
        '''Unzip file and extract in given directory path

        Parameters
        ----------
        filepath : str
            path to file to unzip
        dirpath : str or None, optional, default is None
            directory path where zip file contents will be extracted to,
            if None extract in same directory than zip file
        delete : bool, optional, default is True
            if True, delete the zip file after extraction

        '''
        dirpath = dirpath or os.path.abspath(os.path.dirname(filepath))
        self.logger.info(f'Unzipping file {filepath}')
        with zipfile.ZipFile(filepath, 'r') as f:
            f.extractall(dirpath)

        if delete:
            self.logger.info(f'Removing file {filepath}')
            os.remove(filepath)

    def rename_files_in(self, dirpath):
        '''Rename files from given directory path into generic ones

        Parameters
        ----------
        dirpath : str
            directory path where files will be renamed

        '''
        self.logger.info(f'Reading files in {dirpath}')
        files = os.listdir(dirpath)

        for f in files:
            for dataset in ('train', 'test'):
                if re.match(f'.*_{dataset}.csv', f) is not None:
                    self.logger.info(f'Renaming file {f} into {dataset}.csv')
                    os.rename(os.path.join(dirpath, f), os.path.join(dirpath, f'{dataset}.csv'))
