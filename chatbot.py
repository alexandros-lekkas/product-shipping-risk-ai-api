# General dependencies
import os
import json
from dotenv import load_dotenv

# Langchain dependencies
import bs4
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


conversation_history = []

def get_chatbot_respsonse(user_input, conversation_history):
    model = ChatOpenAI(model="gpt-4o-mini")
    messaages = [
        SystemMessage(content=)
    ]

    

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = openai_api_key

categorizer_model = ChatOpenAI(model="gpt-4o-mini")

conversation_history = []

def blank():
    print("")
    
blank()

while True:
    userInput = input("What would you like to ask our AI? (Type 'exit' to end the conversation): ")

    if userInput.lower() == 'exit':
        print("Ending conversation. Goodbye!")
        break

    conversation_history.append(HumanMessage(content=userInput))

    categorization_messages = [
        SystemMessage(content="""
                      You are an AI assistant for a financial savings company.
                      
                      Categorize this message into one of 4 categories: general, financial, irrelevant.
                      
                      General: queries questions related to the company
                      Financial: questions or conversations related to finance
                      Irrelevant: anything inappropriate or irrelevant to financial application or sensible questions
                      
                      Upon decision of the category, the only thing you will return is JSON. The key will be "category" and the value will be the category that you decide.
                      
                      e.g.
                      {
                        "category": "general"
                      }
                      
                      You will not return any other text.
                      """),
        HumanMessage(content=userInput)
    ]
    
    response = categorizer_model.invoke(categorization_messages)
    print(f"Categorization Response: {response.content}")
    blank()
    
    try:
        parsed_response = json.loads(response.content)
        category = parsed_response['category']
    except json.JSONDecodeError:
        print("Failed to parse the response as JSON. Please try again.")
        continue

    conversation_model = ChatOpenAI(model="gpt-4")

    if category == "general":
        categorizer_model = ChatOpenAI(model="gpt-4")
        system_message = SystemMessage(content="""
                    You are an AI assistant for a financial savings company.
                    
                    You will return 2-3 sentences straight away. No paragraph breaks. Just respond to the user in a general manner.
                    """)
    elif category == "financial":
        categorizer_model = ChatOpenAI(model="gpt-4")
        system_message = SystemMessage(content="""
                    You are an AI assistant for a financial savings company.
                    
                    You are qualified to give excellent financial advice. You are the best financial advisor.
                    """)
    elif category == "irrelevant":
        system_message = SystemMessage(content="""
                    You are an AI assistant for a financial savings company.
                    
                    Please respond saying what your role is, and how you cannot respond to such questions.
                    """)
    else:
        system_message = SystemMessage(content="""
                    You are an AI assistant for a financial savings company.
                    
                    Say you have trouble understanding their request.
                    """)

    conversation_history.append(system_message)

    response = conversation_model.invoke(conversation_history)
    
    print(f"AI Response: {response.content}")
    blank()
    
    conversation_history.append(HumanMessage(content=response.content))