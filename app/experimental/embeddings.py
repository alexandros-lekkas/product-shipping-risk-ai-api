import os
import yaml


def load_file(file_path):
    file_name, file_extension = os.path.splitext(file_path)
    
    with open(file_path, 'r') as file:
        if (file_extension == '.yaml'):
            return yaml.safe_load(file)
        else:
            return file.read()

class EmbeddingsModel:
    def __init__(self):
        self.model = model = OpenAIEmbeddings(api_key=os.getenv('OPENAI_API_KEY'))
        self.data = []
        
    def get_data(self, yaml_file_path):
        file = load_file(yaml_file_path)
        data_array = []
        
        for recommendation in file:
            description = recommendation.get('description')
            message = recommendation.get('message')
            if description:
                print(description)
                data_array.append(message + " " + description)
                self.data.append(recommendation)
                
        self.embeddings = self.model.embed_documents(data_array)
        print(len(self.embeddings), len(self.embeddings[0]))
        
    def query_data(self, query):
        embedded_query = self.model.embed_query(query)
        print(embedded_query)

        similarities = cosine_similarity([embedded_query], self.embeddings)[0]
        sorted_similarity_indices = np.argsort(similarities)
        best_match_index_1 = sorted_similarity_indices[-1]
        best_match_index_2 = sorted_similarity_indices[-2]
        best_match_1 = self.data[best_match_index_1]
        best_match_2 = self.data[best_match_index_2]
        
        print(f"Best match 1:\n{best_match_1['message']}\n- {best_match_1['description']}")
        print("")
        print(f"Best match 2:\n{best_match_2['message']}\n- {best_match_2['description']}")
        return best_match_1, best_match_2
                
if __name__ == '__main__':
    embeddingsModel = EmbeddingsModel()
    
    embeddingsModel.get_data('app/experimental/sr_version_2.yaml')
    
    embeddingsModel.query_data("What is a Cash ISA account?")
    