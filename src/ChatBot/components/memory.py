from ChatBot import logger
from ChatBot.entity.config_entity import MemoryConfig

from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate

class Memory:
    def __init__(self, config: MemoryConfig):
        self.config = config

    def get_chat_chain(self, qna_result):
        """
        Read pincone_upsert_docs config file and store as config entity
        then apply the dataclasses
        
        Returns:
        qa.invoke(query) -> dict: query and the QnA answer
        """
        
        command = """
        %INSTRUCTIONS:
        You are very helpful chatbot.
        Your goal is only write this piece of text.

        %TEXT: {text}
        """

        prompt = PromptTemplate(
            input_variables=["text"],
            template=command,
        )

        command_prompt = prompt.format(text=qna_result['result'])

        # Setup prompt to take human imput and chat history.
        chat = """
        {chat_history}
        Human: {human_input}
        Chatbot:"""

        template = command_prompt + chat
        
        memory = ConversationBufferMemory(memory_key="chat_history")

        prompt = PromptTemplate(
            input_variables=["chat_history", "human_input"], 
            template=template
        )

        chat_chain = LLMChain(
            llm=OpenAI(
                model_name=self.config.llm, 
                openai_api_key=self.config.openai_api_key
            ), 
            memory=memory,
            prompt=prompt, 
            verbose=True
        )
        
        return chat_chain