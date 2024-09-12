import os
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

class AI:
    def __init__(self, model):
        self.model = ChatOpenAI(model)
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