import os
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

class AI:
    natural_language_error_message = 'Unfortunately I ran into some issues with your request, is there anything else I can help with?'
 
    def __init__(self, model_name):
        self.model = ChatOpenAI(model=model_name)
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')                  
            
    def get(self,key,default=None):
        return getattr(self, key, default)
    
    def invoke_simple(self, prompt, input):
        messages = [
            SystemMessage(content = prompt),
            HumanMessage(content = input)
        ]
        
        return self.model.invoke(messages)
    
    def invoke_structured(self, prompt, input, structure):
        structured_model = self.model.with_structured_output(structure)
        
        messages = [
            SystemMessage(content = prompt),
            HumanMessage(content = input)
        ]
        
        return structured_model.invoke(messages)

        