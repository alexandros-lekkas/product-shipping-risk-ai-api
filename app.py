import json
import os
import yaml
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, trim_messages

# Load config YAML
def load_config(config_path='config.yaml'):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

# Load prompt from TXT for organization & reusability
def load_prompt(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Parse a response from AI for JSON
def parse_ai_response(response, key, default):
    try:
        parsed_response = json.loads(response.content)
        key = parsed_response[key]
    except json.JSONDecodeError:
        key = default
        
    return key

# SystemMessage & HumanMessage simple AI call (2 messages in context)
def invoke_model_simple(prompt, content):
    messages = [
        SystemMessage(content=prompt),
        HumanMessage(content=content)
    ]
    response = model.invoke(messages)
    return response
   
app = FastAPI()

# Get advice for a product (could be risk, could be shipping)
class ProductAdviceRequest(BaseModel):
    user_input: str
    item_data: dict
@app.post('/advice/product')
def advice(request: ProductAdviceRequest):
    user_input = request.user_input
    item_data = request.item_data
    
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
        prompt = load_prompt('prompts/estimate_shipping_parameters.txt')
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
        
        # Perform API call
        config = load_config()
        api_url = config['api_calls']['estimate_shipping']['url']
        payload = {
            "country_name": country,
            "weight_g": weight_g,
            "height_cm": height_cm,
            "width_cm": width_cm,
            "length_cm": length_cm
        }
        response = requests.post(api_url, json=payload)
        
        if response.status_code == 200: # Successful execution (calculation happened)
            api_response_data = response.json()
            
            prompt = load_prompt('prompts/shipping_results_received.txt')
            response = invoke_model_simple(prompt, f'User Message: {user_input}\nItem Data: {item_data}')
            return response.content
        else: # There was an error
            return natural_language_error_message

# Main func to run when script is loaded
if __name__ == '__main__':
    config = load_config()
    
    os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
    model = ChatOpenAI(model=config['openai']['model'])
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=config['debug'])