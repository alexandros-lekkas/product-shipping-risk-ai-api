from app.utils.file import load_file
from app.models.ai import AI
from app.prompts.plum import plum, Plum

def compare_models():
    file_name = 'sr_version_2.yaml'
    data = load_file(file_name)
    
    ai = AI("gpt-4o-mini", True, True)
    
    exit = False
    while not exit:
        query = input("Query: ")
        
        # Find match with embeddings
        ai.embeddings_get_data(file_name , ['message', 'description'])
        index_1, index_2 = ai.embeddings_query_data()
        embeddings_results = f'[Embeddings Results]\n1:{data[index_1]}\n2:{data[index_2]}\n'
        print(embeddings_results)
        
        # Find match with LLM
        response = ai.llm_invoke_structured(plum, query, Plum)
        llm_results = f'[LLM Results]\n1:{data[response.best_match_1]}\n2:{data[response.best_match_2]}\n'
        print(llm_results)
        
        return f'{embeddings_results}\n{llm_results}'