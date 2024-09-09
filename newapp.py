import json
import os
import yaml
from flask import Flask, request, jsonify
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, trim_messages

def load_config(config_path='config.yaml'):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

app = Flask(__name__) 

@app.route("/advice/product", methods=['POST'])
def advice():
    user_input = request.form['user_input']
    item_data = request.form['item_data']
    
    item_data = json.loads(item_data)
    
    messages = []
    api_call = "none"
    
    if item_data:
        messages = {
            SystemMessage(content = (
                "You are an AI assistant who's role is to determine if an API call is needed based on a message."
                "API calls are these options: estimate_shipping, none"
                "When you determine the api_call you will return it as json"
                "e.g { 'api_call': 'estimate_shipping'} <- you must only respond with this JSON"
                "For example, if you get the json of an item data, and the user also says 'what is the estimated shipping to greece'?"
                "In this case the API call will be estimate_shipping"
                "If the user asks"
            ))
        }
        
        

if __name__ == '__main__':
    config = load_config()
    
    os.environ["OPENAI_API_KEY"] = os.getenv("OEPNAI_API_KEY")
    model = ChatOpenAI(model=config['openai']['model'])
    
    app.run(config['debug'])