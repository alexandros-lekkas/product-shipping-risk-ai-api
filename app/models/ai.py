import os
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

class AI:
    natural_language_error_message = 'Unfortunately I ran into some issues with your request, is there anything else I can help with?'
 
    def __init__(self, model_name):
        self.model = ChatOpenAI(model=model_name)
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')                  
            
    def get(self,key,default=None):
        return getattr(self, key, default)
    
    def invoke_model_simple(self, prompt, content):
        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content=content)
        ]
        
        response = self.model.invoke(messages)
        return response
    
    def parse_ai_response(self, response, key, default):
        try:
            parsed_response = json.loads(response.content)
            key = parsed_response.get(key, default)
        except json.JSONDecodeError:
            key = default
            
        return key
    
    def invoke_and_parse_model_response(self, prompt, content, key, default):
        response = self.invoke_model_simple(prompt, content)
        return self.parse_ai_response(response, key, default)