import json
import os
import yaml
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, trim_messages
from rich.console import Console

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

# Initialize console
console = Console()

# Initialize config and FastAPI
config = load_config()
app = FastAPI(debug=config['debug'])

# Initialize OpenAI model globally (accessible by all methods and API calls)
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
model = ChatOpenAI(model=config['openai']['model'])

# Get advice for a product (could be risk, could be shipping)
class ProductAdviceRequest(BaseModel):
    user_input: str
    item_data: dict
@app.post('/advice/product')
def advice(request: ProductAdviceRequest):
    user_input = request.user_input
    item_data = request.item_data
    
    # Perform API call categorization call
    prompt = load_prompt('prompts/api_call_determination.txt')
    response = invoke_model_simple(prompt, f'User Message: {user_input}\nItem Data: {item_data}')
    api_call = parse_ai_response(response, 'api_call', 'none')
    console.print('[bold green]Response (Categorization):[/bold green]',response.content)
    
    # Seperate functionality (based on determined API call)
    if api_call == 'none': # None / No API Call
        prompt = load_prompt('prompts/no_call.txt')
        response = invoke_model_simple(prompt, f'User Message: {user_input}\nItem Data: {item_data}')
        console.print('[bold green]Response (No Call):[/bold green]',response.content)
        return response.content
    elif api_call == 'estimate_shipping': # Estimate Shipping
        prompt = load_prompt('prompts/estimate_shipping_parameters.txt')
        response = invoke_model_simple(prompt, f'User Message: {user_input}\nItem Data: {item_data}')
        console.print('[bold green]Response (Estimate Shipping):[/bold green]',response.content)

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
                console.print('[bold red]Issues:[/bold red]',natural_language_error_message)
                return natural_language_error_message
        
        # Perform API call
        config = load_config()
        api_url = config['api_calls']['estimate_shipping']['url']
        payload = {
            "country": country,
            "weightg": weight_g,
            "heightcm": height_cm,
            "widthcm": width_cm,
            "lengthcm": length_cm
        }
        headers = {
            'Content-Type': 'application/json',
            'apiKey': os.getenv("SUPABASE_ANON_API_KEY"),
            'Authorization': f'Bearer {os.getenv("SUPABASE_ANON_BEARER_TOKEN")}'
        }
        response = requests.post(api_url, json=payload, headers=headers)
        console.print('[bold green]Response (Shipping Results Received):[/bold green]',response.content)
        
        if response.status_code == 200: # Successful execution (calculation happened)
            api_response_data = response.json()
            
            prompt = load_prompt('prompts/shipping_results_received.txt')
            response = invoke_model_simple(prompt, f'User Message: {user_input}\nShipping Results: {api_response_data}')
            console.print('[bold green]Response (Shipping Results Received):[/bold green]',response.content)
            return response.content
        else: # There was an error
            console.print('[bold red]Issues:[/bold red]',natural_language_error_message)
            return natural_language_error_message

# Main func to run when script is loaded
if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=config['reload'])