import json
import os
import yaml
from flask import Flask, request, jsonify
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, trim_messages

def load_config(config_path='config.yaml'):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)
    
def load_prompt(file_path):
    with open(file_path, 'r') as file:
        return file.read()
    
def parse_ai_response(response, key, default):
    try:
        parsed_response = json.loads(response.content)
        key = parsed_response[key]
    except json.JSONDecodeError:
        key = default
        
    return key
    
app = Flask(__name__) 

@app.route("/advice/product", methods=['POST'])
def advice():
    user_input = request.form['user_input']
    item_data = request.form['item_data']
    
    item_data = json.loads(item_data)
        
    messages = [
        SystemMessage(content=(load_prompt("prompts/api_call_determination.txt"))),
        HumanMessage(content=f"User Message: {user_input}\nItem Data: {item_data}")
    ]
    response = model.invoke(messages)
    api_call = parse_ai_response(response, 'api_call', 'none')
    
    if api_call == "none":
        prompt = load_prompt("prompts/no_call.txt")
    elif api_call == "estimate_shipping": # Subject to change + API call in background
        prompt = load_prompt("prompts/no_call.txt")
 
    messages = [
        SystemMessage(content=prompt),
        HumanMessage(content=f"User Message: {user_input}\nItem Data: {item_data}")
    ]
    response = model.invoke(messages)
    return response.content

if __name__ == '__main__':
    config = load_config()
    
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    model = ChatOpenAI(model=config['openai']['model'])
    
    app.run(debug=config['debug'])