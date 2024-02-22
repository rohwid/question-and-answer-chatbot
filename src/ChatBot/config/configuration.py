import os

from pathlib import Path
from CNNClassifier.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from CNNClassifier.utils.common import read_yaml, create_directories
class ConfigurationManager:
    def __init__(self, 
                 config_filepath = CONFIG_FILE_PATH,
                 params_filepath = PARAMS_FILE_PATH):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])
    
    def get_data_ingestion_gdrive_config(self) -> DataIngestionGDriveConfig:
        """
        Read data_ingestion config file and store as config entity
        then apply the dataclasses
        """
        config = self.config.ingest_data_from_gdrive

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionGDriveConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir,
            unzip_data=config.unzip_data
        )

        return data_ingestion_config