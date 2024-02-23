import os
import gdown

from ChatBot import logger
from ChatBot.entity.config_entity import DataIngestionGDriveConfig

class DataIngestionGDrive:
    def __init__(self, config: DataIngestionGDriveConfig):
        self.config = config

    def download_file(self):
        """
        Download data from GDrive
        
        Raises:
            e: Error when try to connect GDrive.
        """
        try: 
            dataset_url = self.config.source_URL
            download_dir = self.config.local_data_dir
            download_file = self.config.local_data_file
            force_ingest = self.config.force_ingest
            
            file_exist = os.path.exists(download_file)
            
            if not file_exist or force_ingest:
                os.makedirs(download_dir, exist_ok=True)
                logger.info(f"Downloading data from {dataset_url} into file {download_file}")

                file_id = dataset_url.split("/")[-2]
                prefix = 'https://drive.google.com/uc?/export=download&id='
                gdown.download(prefix+file_id, download_file)

                logger.info(f"Downloaded data from {dataset_url} into file {download_file}")
            else:
                logger.info(f"File {download_file} exist, download skipped.")

        except Exception as e:
            raise e