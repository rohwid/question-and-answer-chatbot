from ChatBot import logger
from ChatBot.pipeline.stage_02_upsert_documents import PinconeUpsertDocsLLMPipeline

STAGE_NAME = "Pincone Upsert Documents"

try:
    logger.info(f"\n\n")
    logger.info(f">>>>>>> Stage {STAGE_NAME} Started <<<<<<< ".upper())
    
    obj = PinconeUpsertDocsLLMPipeline()
    obj.pipeline()
    
    logger.info(f">>>>>>> Stage {STAGE_NAME} Completed <<<<<<< ]\n\n".upper())
except Exception as e:
    logger.exception(e)
    raise e