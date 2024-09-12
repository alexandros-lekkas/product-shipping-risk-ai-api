from app.models.ai import AI
from app.api.supabase import estimate_shipping
from app.prompts.api_call_determination import api_call_determination, APICallDetermination
from app.prompts.no_call import no_call
from app.prompts.estimate_shipping_parameters import estimate_shipping_parameters, EstimatedShippingParameters
from app.prompts.shipping_results_received import shipping_results_received

def get_advice(user_input, item_data):
    input_string = f'User Message: {user_input}\nItem Data: {item_data}'
    
    ai = AI("gpt-4o-mini")
    
    response = ai.invoke_structured(api_call_determination, input_string, APICallDetermination)
    
    if response.api_call == 'none': return ai.invoke_model_simple(no_call, input_string).content
    elif response.api_call == 'estimate_shipping':
        response = ai.invoke_structured(estimate_shipping_parameters, input_string, EstimatedShippingParameters)
            
        response = estimate_shipping(response.country,
                                     response.weight_g,
                                     response.height_cm,
                                     response.length_cm,
                                     response.width_cm)
        
        if response.status_code == 200:
            api_response_data = response.json()
            
            return ai.invoke_simple(shipping_results_received, input_string)
        else:
            return AI.natural_language_error_message
