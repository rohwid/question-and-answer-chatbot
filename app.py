from ChatBot.components.qna import QnA
from ChatBot.components.memory import Memory
from ChatBot.config.configuration import ConfigurationManager


config = ConfigurationManager()
qna_config = config.get_qna_config()
qna = QnA(qna_config)

query = "What are the specific features or aspects that users appreciate the most in our application?"
qna_result = qna.get_qna_chain(query)

memory_config = config.get_memory_config()
chat = Memory(memory_config)

chat_reply = chat.get_chat_chain(qna_result, query)
print(chat_reply)