from ChatBot.config.configuration import ConfigurationManager
from ChatBot.components.upsert_documents import PinconeUpsertDocs
from ChatBot import logger
from pinecone import Pinecone

import random


STAGE_NAME = "Pincone Upsert Documents"

class PinconeUpsertDocsLLMPipeline:
    def __init__(self):
        pass

    def pipeline(self):
        config = ConfigurationManager()
        pincone_upsert_docs_config = config.get_pincone_upsert_docs_config()
        
        PINECONE_API_KEY = pincone_upsert_docs_config.pincone_api_key
        PINECONE_INDEX = pincone_upsert_docs_config.pincone_index
        namespace = pincone_upsert_docs_config.namespace
        id_prefix = pincone_upsert_docs_config.id_prefix
        force_upsert = pincone_upsert_docs_config.force_upsert
        
        pincone = Pinecone(api_key=PINECONE_API_KEY)
        index = pincone.Index(PINECONE_INDEX)
        
        random_ids = random.sample(range(0, 100), 3)
        ids = [f'{id_prefix}-{id}' for id in random_ids]

        docs_not_exist = True
        
        while ids:
            try:
                result = index.fetch(ids=[ids.pop()], namespace=namespace)
            except Exception as err:
                raise(err)
            else:
                if result['vectors']:
                    docs_not_exist = False
        
        if docs_not_exist or force_upsert:
            pincone_upsert_docs = PinconeUpsertDocs(config=pincone_upsert_docs_config)
            pincone_upsert_docs.upsert_docs()

if __name__ == '__main__':
    try:
        logger.info(f"\n\n")
        logger.info(f">>>>>>> Stage {STAGE_NAME} Started <<<<<<<")
        
        obj = PinconeUpsertDocsLLMPipeline()
        obj.pipeline()
        
        logger.info(f">>>>>> Stage {STAGE_NAME} Completed <<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e