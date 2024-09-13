import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage
from app.utils.file import load_file, load_structured_yaml_file

class AI:
    natural_language_error_message = 'Unfortunately I ran into some issues with your request, is there anything else I can help with?'
 
    def __init__(self, model_name, llm, embeddings):
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        
        if llm:
            self.llm_model = ChatOpenAI(model=model_name)
        if embeddings:
            self.embeddings_model = OpenAIEmbeddings(self.OPENAI_API_KEY)        
                       
    def get(self,key,default=None):
        return getattr(self, key, default)
    
    def llm_invoke_simple(self, prompt, input):
        messages = [
            SystemMessage(content = prompt),
            HumanMessage(content = input)
        ]
        
        return self.llm_model.invoke(messages)
    
    def llm_invoke_structured(self, prompt, input, structure):
        structured_llm_model = self.llm_model.with_structured_output(structure)
        
        messages = [
            SystemMessage(content = prompt),
            HumanMessage(content = input)
        ]
        
        return structured_llm_model.invoke(messages)
    
    def embeddings_get_data(self, file_path, fields):
        