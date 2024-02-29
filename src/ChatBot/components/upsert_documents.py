import os
import pandas as pd

from ChatBot import logger
from ChatBot.entity.config_entity import PineconeUpsertDocsConfig

from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import Pinecone

class PinconeUpsertDocs:
    def __init__(self, config: PineconeUpsertDocsConfig):
        self.config = config

    def upsert_docs(self):
        """
        Upsert data to Pincone vector database.
        
        Raises:
            e: Error when try to use OpenAI API 
               or connect Pincone Database.
        """
        logger.info(f"Reading dataset.")
        df = pd.read_csv(self.config.local_data_file)
        df.rename(
            columns = {'review_text':'google_store_review_comments'}, 
            inplace = True
        ) 
        
        logger.info(f"Creating new dataset to load.")
        csvloader_df = None
        
        if self.config.data_length > 0:
            csvloader_df = df.iloc[0:self.config.data_length, 1:]
        else:
            csvloader_df = df[df.columns[1:]]
            
        csvloader_df.to_csv(self.config.load_data_file, index=False)
        
        logger.info(f"Loading all CSV rows as documents.")
        loader = CSVLoader(
            file_path=self.config.load_data_file, 
            source_column=self.config.source_column, 
            metadata_columns=self.config.metadata_column
        )
        csvloader_data = loader.load()
        
        logger.info(f"Splitting the documents.")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )
        docs = text_splitter.split_documents(csvloader_data)
        ids = [f'{self.config.id_prefix}-{i}' for i in range(len(docs))]
        
        try:
            logger.info(f"Embedding the documents.")
            embeddings = OpenAIEmbeddings(
                model=self.config.embedding_model, 
                dimensions=self.config.document_dimension
            )
            
            logger.info(f"Uploading the documents to Pincone Database.")
            Pinecone.from_documents(
                docs, 
                embeddings, 
                index_name=self.config.pincone_index, 
                namespace=self.config.namespace, 
                ids=ids
            )
        except Exception as e:
            raise(e)