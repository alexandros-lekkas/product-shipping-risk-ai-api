import os
import requests

def estimate_shipping(country, weight_g, height_cm, width_cm, length_cm):
    api_url = 'https://qiyrhobdkqezshwhokmw.supabase.co/rest/v1/rpc/calculateshippingcost'
    
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