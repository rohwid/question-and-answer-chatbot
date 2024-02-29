from dataclasses import dataclass

from langchain.chains import LLMChain
from langchain_openai import OpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate

from ChatBot.components.qna import QnA
from ChatBot.config.configuration import ConfigurationManager

import streamlit as st

config = ConfigurationManager()
qna_config = config.get_qna_config()
memory_config = config.get_memory_config()

USER = "user"
ASSISTANT = "ai"
MESSAGES = "messages"
LLM_CHAIN = "llm_chain"

@dataclass
class Message:
    actor: str
    payload: str

@st.cache_resource
def get_llm() -> OpenAI:
    """
    Set OPENAI model as streamlit cache
    
    Returns:
        OPENAI (obj): object to load OPENAI model
    """
    return OpenAI(
        model_name=memory_config.llm, 
        openai_api_key=memory_config.openai_api_key
    )

def get_qna_chain_in_session(query):
    """
    Load query and proced by Langchain QnA chain
    
    Returns:
        custom_prompt (str): custom prompt as the result of QnA
    """
    qna = QnA(qna_config)
    qna_chain = qna.get_qna_chain(query)
    ref = qna_chain.invoke(query)
    custom_prompt = """
    {query} And you can use \"{ref}\" as reference.
    """.format(
        query=query.strip(),
        ref=ref['result'].strip()
    )
    return custom_prompt

def get_llm_chain():
    """
    Chat session with langchain memory and LLMChain
    
    Returns:
        conversation (obj): LLMChain object with prompt and memory
    """
    template = """
    You are very helpful chatbot.

    Previous conversation:
    {chat_history}

    New human question: {question}
    Response: """
    prompt_template = PromptTemplate.from_template(template)
    
    memory = ConversationBufferWindowMemory(memory_key="chat_history", k=3)
    conversation = LLMChain(
        llm=get_llm(),
        prompt=prompt_template,
        verbose=True,
        memory=memory
    )
    return conversation

def initialize_session_state():
    """
    Initialize the message and model in LLMChain object
    """
    if MESSAGES not in st.session_state:
        st.session_state[MESSAGES] = [Message(actor=ASSISTANT, payload="Hi!How can I help you?")]
    if LLM_CHAIN not in st.session_state:
        st.session_state[LLM_CHAIN] = get_llm_chain()

def get_llm_chain_from_session() -> LLMChain:
    """
    Call the model in LLMChain object to answer the question
    """
    return st.session_state[LLM_CHAIN]

initialize_session_state()

msg: Message
for msg in st.session_state[MESSAGES]:
    st.chat_message(msg.actor).write(msg.payload)

prompt: str = st.chat_input("Enter a prompt here")

if prompt:
    st.session_state[MESSAGES].append(Message(actor=USER, payload=prompt))
    st.chat_message(USER).write(prompt)

    with st.spinner("Please wait.."):
        custom_prompt = get_qna_chain_in_session(prompt)
        llm_chain = get_llm_chain_from_session()
        response: str = llm_chain({"question": custom_prompt})["text"]
        
        st.session_state[MESSAGES].append(Message(actor=ASSISTANT, payload=response))
        st.chat_message(ASSISTANT).write(response)