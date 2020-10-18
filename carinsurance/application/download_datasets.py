import os

from carinsurance import logger
from carinsurance.config import CONFIG
from carinsurance.infrastructure.dataset import CarInsuranceDataset


def download_datasets(config, logger):
    project_path = config['project']
    data_path = os.path.join(project_path, config['data'])
    raw_path = os.path.join(data_path, 'raw')

    if not os.path.exists(raw_path):
        logger.info('Creating raw directory...')
        os.makedirs(raw_path, exist_ok=True)

    dataset = CarInsuranceDataset(logger=logger)
    dataset.download(filepath=raw_path)
    dataset.unzip(filepath=os.path.join(raw_path, dataset.zipname), delete=True)
    dataset.rename_files_in(raw_path)


if __name__ == '__main__':
    download_datasets(CONFIG, logger)
