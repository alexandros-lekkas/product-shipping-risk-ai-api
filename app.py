import json
import os
import yaml
import requests
from flask import Flask, request, jsonify, request
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

def invoke_model_simple(prompt, content):
    messages = [
        SystemMessage(content=prompt),
        HumanMessage(content=content)
    ]
    response = model.invoke(messages)
    return response
   
app = Flask(__name__) 

# Get advice for a product (could be risk, could be shipping)
@app.route('/advice/product', methods=['POST'])
def advice():
    user_input = request.form['user_input']
    item_data = request.form['item_data']
    
    item_data = json.loads(item_data)
    
    # Perform API call categorization call
    load_prompt('prompts/api_call_determination.txt')
    response = invoke_model_simple(prompt, f'User Message: {user_input}\nItem Data: {item_data}')
    api_call = parse_ai_response(response, 'api_call', 'none')
    
    # Seperate functionality (based on determined API call)
    if api_call == 'none': # None / No API Call
        prompt = load_prompt('prompts/no_call.txt')
        response = invoke_model_simple(prompt, f'User Message: {user_input}\nItem Data: {item_data}')
        return response
    elif api_call == 'estimate_shipping': # Estimate Shipping
        prompt = load_prompt('estimate_shipping_parameters.txt')
        response = invoke_model_simple(prompt, f'User Message: {user_input}\nItem Data: {item_data}')

        natural_language_error_message = 'Unfortunately I ran into some issues while attempting to estimate the shipping for this item. Is there anything else I can help with?'
                
        # Parse the AI response for the estimated values (needed for shipping estimation)
        country = parse_ai_response(response, 'country', '')
        weight_g = parse_ai_response(response, 'weight_g', '')
        height_cm = parse_ai_response(response, 'height_cm', '')
        length_cm = parse_ai_response(response, 'length_cm', '')
        width_cm = parse_ai_response(response, 'width_cm', '')
        
        # Ensure all values are parsed correctly
        keys = [country, weight_g, height_cm, length_cm, width_cm]
        for key in keys:
            if (key == ''):
                return natural_language_error_message
        
        # Perform API call to estimate shipping cost
        api_url = 
        data = {
            title
        }
        response = requests.post(api_url)
        
        if response.status_code == 200:
            api_response_data = response.json()
            print(jsonify(api_response_data))
            
            
        else:
            return 
 


if __name__ == '__main__':
    config = load_config()
    
    os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
    model = ChatOpenAI(model=config['openai']['model'])
    
    app.run(debug=config['debug'])