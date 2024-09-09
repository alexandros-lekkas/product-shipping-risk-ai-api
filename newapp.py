import json
import os
import yaml
from flask import Flask, request, jsonify
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, trim_messages

# Configuration loader
def load_config(config_path='config.yaml'):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

@app.route("/advice/product", methods=['POST'])
def advice():
    user_input = request.form['user_input']
    item_data = request.form['item_data']
    
    item_data = json.loads(item_data)
    
    messages = []
    
    if item_data:
        messages = {
            SystemMessage(content = (
                
            ))
        }
    else:
        print("")
 
app = Flask(__name__) 
if __name__ == '__main__':
    config = load_config()
    
    os.environ["OPENAI_API_KEY"] = os.getenv("OEPNAI_API_KEY")
    model = ChatOpenAI(model=config['openai']['model'])
    
    app.run(config['debug'])