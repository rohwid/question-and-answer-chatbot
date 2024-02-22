from ChatBot.components.qna import QnA
from ChatBot.components.memory import Memory
from ChatBot.config.configuration import ConfigurationManager

import streamlit as st

config = ConfigurationManager()

def qna_chain(query):
    qna_config = config.get_qna_config()
    qna = QnA(qna_config)
    qna_chain = qna.get_qna_chain(query)
    return qna_chain

def chat_chain(qna_result):
    memory_config = config.get_memory_config()
    chat = Memory(memory_config)
    chat_chain = chat.get_chat_chain(qna_result)
    return chat_chain

st.set_page_config(
    page_title="ChatGPT Clone",
    page_icon="🤖",
    layout="wide"
)


st.title("ChatGPT Clone")

# check for messages in session and create if not exists
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "Hello there, am ChatGPT clone"
        }
    ]

# Display all messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


user_prompt = st.chat_input()

if user_prompt is not None:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.write(user_prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Loading..."):
            qna_chain = qna_chain(user_prompt)
            qna_result = qna_chain.invoke(user_prompt)
            
            chat_chain = chat_chain(qna_result)
            ai_response = chat_chain.predict(human_input=f'{user_prompt}')
            
            st.write(ai_response)
    new_ai_message = {"role": "assistant", "content": ai_response}
    st.session_state.messages.append(new_ai_message)