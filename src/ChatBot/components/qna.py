import os

from ChatBot import logger
from ChatBot.entity.config_entity import QnAConfig

from pinecone import Pinecone
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_pinecone import Pinecone as LangchainPinecone
from langchain.chains import RetrievalQA

class QnA:
    def __init__(self, config: QnAConfig):
        self.config = config

    def get_qna_chain(self, query):
        """
        Read pincone_upsert_docs config file and store as config entity
        then apply the dataclasses
        
        Returns:
        qa.invoke(query) -> dict: query and the QnA answer
        """
        pincone = Pinecone(api_key=self.config.pincone_api_key)
        index = pincone.Index(self.config.pincone_index)
        
        embeddings = OpenAIEmbeddings(
            model=self.config.embedding_model, 
            dimensions=self.config.document_dimension
        )
        
        text_field = "text"
        vectorstore = LangchainPinecone(
            index, embeddings, text_field, namespace=self.config.namespace
        )
        
        vectorstore.similarity_search(
            query,  # our search query
            k=5  # return 3 most relevant docs
        )
        
        llm = OpenAI(
            temperature=self.config.temperature, 
            model_name=self.config.llm, 
            openai_api_key=self.config.openai_api_key
        )
        
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever()
        )

        return qa.invoke(query)
        