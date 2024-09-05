import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, trim_messages

# LLM configuration
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
model = ChatOpenAI(model="gpt-3.5-turbo")
starterLine = "You are an AI financial assistant. Your purpose is to assist users with chats primarily related to finance."

# Message history config (trimmer)
trimmer = trim_messages(
    max_tokens=125,
    strategy="last",
    token_counter=model,
    include_system=True,
    allow_partial=False,
    start_on="human"
)

# Basic chat function
def chat(user_input, messages):
    if messages:
        messages = trimmer.invoke(messages)
    else:
        print("No reason to trim messages.")
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
        
    # Use categorized system message
    if category == "GENERAL":
        new_system_message = (
            starterLine + "\n"
            "Message category: GENERAL"
            "Please answer the human's discussion generally. Not in strict financial terms, but finance related."
        )
        messages = update_system_message(messages, new_system_message)
    elif category == "FINANCE":
        new_system_message = (
            starterLine + "\n"
            "Message category: FINANCE"
            "The user/human requests financial discussion, you discuss simply but try to keep things digestible for the user and speak strictly on finance."
        )
        messages = update_system_message(messages, new_system_message)
    elif category == "RANDOM":
        new_system_message = (
            starterLine + "\n"
            "Message category: RANDOM"
            "The user has insulted you by saying something utterly random. Tell them you are a financial assistant and will not indulge in their nonsense."
            "End your sentences with:"
            '"You got no money, you got no honey, and that is, not funny."'
        )
        messages = update_system_message(messages, new_system_message)
    elif category == "UNKNOWN":
        new_system_message = (
            starterLine + "\n"
            "Message category: UNKNOWN"
            "For some reason the user's message was not categorized."
            "Answer to the best of your ability, try to keep messages finance related."
        )
        messages = update_system_message(messages, new_system_message)
    else:
        new_system_message = (
            "An error has occured, please inform the human to inform customer support."
        )
        messages = update_system_message(messages, new_system_message)
    
    # Generate and return response and updated messages
    response = model.invoke(messages)
    messages.append(AIMessage(content={response.content}))
    messages.append(HumanMessage(content=user_input))
    return messages, {response.content}
        

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