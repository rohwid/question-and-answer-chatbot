import os
import gdown

from ChatBot import logger
from ChatBot.entity.config_entity import DataIngestionGDriveConfig

class DataIngestionGDrive:
    def __init__(self, config: DataIngestionGDriveConfig):
        self.config = config

    def download_file(self):
        """
        Fetch data from the url
        """
        try: 
            dataset_url = self.config.source_URL
            zip_download_dir = self.config.local_data_file
            os.makedirs("artifacts/data_ingestion", exist_ok=True)
            logger.info(f"Downloading data from {dataset_url} into file {zip_download_dir}")

            file_id = dataset_url.split("/")[-2]
            prefix = 'https://drive.google.com/uc?/export=download&id='
            gdown.download(prefix+file_id, zip_download_dir)

            logger.info(f"Downloaded data from {dataset_url} into file {zip_download_dir}")

        except Exception as e:
            raise e