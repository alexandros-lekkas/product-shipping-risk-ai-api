import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, trim_messages

# LLM configuration
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
model = ChatOpenAI(model="gpt-3.5-turbo")

# Message history config (trimmer)
trimmer = trim_messages(
    max_tokens=65,
    strategy="last",
    token_counter=model,
    include_system=True,
    allow_partial=False,
    start_on="human"
)

# Basic chat function
def chat(user_input, messages):
    messages = trimmer.invoke(messages)
    messages.append(HumanMessage(content=user_input))
    
    # Categorize incoming message
    categorizer_messages = [
        SystemMessage(content = (
            "You are an AI assistant that categorizes messages and returns JSON."
            "Messages can be in one of 3 categories: FINANCE, GENERAL, RANDOM"
            "e.g. { 'category': 'general'} <- this is how you must respond"
        )),
        HumanMessage(content = user_input)
    ]
    response = model.invoke(categorizer_messages)
    try:
        parsed_response = json.loads(response.content)
        category = parsed_response['category']
    except json.JSONDecodeError:
        category = "UNKNOWN"
        
    # Actually respond
    if category == "GENERAL":
        new_system_message = (
            
        )
        messages = update_system_message(messages, new_system_message)
    elif category == "FINANCE":
        new_system_message = (
            
        )
        messages = update_system_message(messages, new_system_message)
    elif category == "RANDOM":
        new_system_message = (
            
        )
        messages = update_system_message(messages, new_system_message)
    elif category == "UNKNOWN":
        new_system_message = (
            
        )
        messages = update_system_message(messages, new_system_message)
    else:
        new_system_message = (
            
        )
        messages = update_system_message(messages, new_system_message)

# Update system message in chat history
def update_system_message(messages, new_system_message):
    found = False
    for message in messages:
        if isinstance(message, SystemMessage):
            message.content = new_system_message
            found = True
            break
    
    # Insert system message if none is found
    if not found:
        messages.insert(0, SystemMessage(content=new_system_message))
        
    return messages
    