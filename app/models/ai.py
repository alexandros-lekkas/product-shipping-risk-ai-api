from app.prompts.plum import plum, Plum
from app.utils.file import load_file, load_structured_yaml_file

import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage

class AI:
    natural_language_error_message = 'Unfortunately I ran into some issues with your request, is there anything else I can help with?'
 
    def __init__(self, model_name, llm, embeddings):
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        
        if llm:
            self.llm_model = ChatOpenAI(model=model_name)
        if embeddings:
            self.embeddings_model = OpenAIEmbeddings(self.OPENAI_API_KEY)    
            
        if not llm and not embeddings:
            self.llm_model = ChatOpenAI(model=model_name)
            
            print("Forcefully creating LLM model, you must pick a model!") 
                       
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
        data = load_structured_yaml_file(file_path, fields)
        
        self.original_data = data
        self.embedded_data = self.embeddings_model.embed_documents(data)
    
    def embeddings_query_data(self, query):
        embedded_query = self.embeddings_model.embed_query(query)
        
        similarities = cosine_similarity([embedded_query], self.embedded_data)[0]
        sorted_similarity_indices = np.argsort(similarities)
        best_match_index_1 = sorted_similarity_indices[-1]
        best_match_index_2 = sorted_similarity_indices[-2]
        
        return best_match_index_1, best_match_index_2