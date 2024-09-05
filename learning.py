# General dependencies
import os
import json
from dotenv import load_dotenv

# Langchain dependencies
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# LLM configuration
store = {}
model = ChatOpenAI(model="gpt-3.5-turbo")
config = {"configurable": {"session_id": "1"}}

# Configure History
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]
with_message_history = RunnableWithMessageHistory(model, get_session_history)
response = with_message_history.invoke(
    [HumanMessage(content="Hey!")],
    config=config
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helfpul assistant. Test"
        ),
        MessagesPlaceholder(variable_name="messages")
    ]
)
chain = prompt | model

response = chain.invoke({"messages": [HumanMessage(content="Hi!")]})