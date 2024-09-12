from app.models.ai import AI
from app.api.supabase import estimate_shipping
from app.prompts.api_call_determination import api_call_determination
from app.prompts.no_call import no_call
from app.prompts.estimate_shipping_parameters import estimate_shipping_parameters
from app.prompts.shipping_results_received import shipping_results_received

def get_advice(user_input, item_data):
    input_string = f'User Message: {user_input}\nItem Data: {item_data}'
    
    ai = AI("gpt-4o-mini")
    
    api_call = AI.invoke_and_parse_model_response(api_call_determination, input_string, 'api_call', 'none')
    
    if api_call == 'none': return AI.invoke_model_simple(no_call, input_string).content
    elif api_call == 'estimate_shipping':
        response = AI.invoke_model_simple(estimate_shipping_parameters, user_input)
        
        country = AI.parse_ai_response(response, 'country', '')
        weight_g = AI.parse_ai_response(response, 'weight_g', '')
        height_cm = AI.parse_ai_response(response, 'height_cm', '')
        length_cm = AI.parse_ai_response(response, 'length_cm', '')
        width_cm = AI.parse_ai_response(response, 'width_cm', '')
        
        keys = [country, weight_g, height_cm, length_cm, width_cm]
        for key in keys:
            if (key == ''):
                return AI.natural_language_error_message
            
        response = estimate_shipping(country, weight_g, height_cm, length_cm, width_cm)
        if response.status_code == 200:
            api_response_data = response.json()
            
            return AI.invoke_model_simple(shipping_results_received, input_string)
        else:
            return AI.natural_language_error_message
