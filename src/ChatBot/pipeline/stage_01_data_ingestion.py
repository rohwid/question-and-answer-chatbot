from ChatBot import logger
from ChatBot.config.configuration import ConfigurationManager
from ChatBot.components.data_ingestion import DataIngestionGDrive

STAGE_NAME = "Data Ingestion"

class DataIngestionLLMPipeline:
    def __init__(self):
        pass

    def gdrive_pipeline(self):
        """
        Download data from GDrive.
        """
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_gdrive_config()
        data_ingestion = DataIngestionGDrive(config=data_ingestion_config)
        data_ingestion.download_file()

if __name__ == '__main__':
    try:
        logger.info(f"\n\n")
        logger.info(f">>>>>>> Stage {STAGE_NAME} Started <<<<<<<")
        
        obj = DataIngestionLLMPipeline()
        obj.gdrive_pipeline()
        
        logger.info(f">>>>>> Stage {STAGE_NAME} Completed <<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e