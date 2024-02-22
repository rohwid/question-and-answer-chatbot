import os

from pathlib import Path
from ChatBot.constants import CONFIG_FILE_PATH
from ChatBot.utils.common import read_yaml, create_directories
from ChatBot.entity.config_entity import (DataIngestionGDriveConfig,
                                          PineconeUpsertDocsConfig)

class ConfigurationManager:
    def __init__(self, config_filepath = CONFIG_FILE_PATH):
        self.config = read_yaml(config_filepath)
        
    def get_data_ingestion_gdrive_config(self) -> DataIngestionGDriveConfig:
        """
        Read data_ingestion config file and store as config entity
        then apply the dataclasses
        
        Returns:
        data_ingestion_config: Config for data ingestion
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
    
    def get_pincone_upsert_docs_config(self) -> PineconeUpsertDocsConfig:
        """
        Read data_ingestion config file and store as config entity
        then apply the dataclasses
        
        Returns:
        pincone_upsert_config: Config for data ingestion
        """
        config = self.config.pincone_upsert_docs

        pincone_upsert_config = PineconeUpsertDocsConfig(
            local_data_file=Path(config.local_data_file),
            load_data_file=Path(config.load_data_file),
            openai_api_key=os.environ.get('OPENAI_API_KEY'),
            pincone_api_key=os.environ.get('PINECONE_API_KEY'),
            pincone_index=os.environ.get('PINECONE_INDEX'),
            data_length=config.data_length,
            source_column=config.source_column,
            metadata_column=config.metadata_column,
            namespace=config.namespace,
            embedding_model=config.embedding_model,
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            document_dimension=config.document_dimension,
            id_prefix=config.id_prefix,
            force_upsert=config.force_upsert
        )
        
        pincone_upsert_config.metadata_column

        return pincone_upsert_config