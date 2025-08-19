from rag.retriever import Retriever
from rag.generator import Generator
class RAGPipeline:
    def __init__(self):
        self.retriever=Retriever()
        self.generator=Generator()

    def query(self,user_query:str, name_space:str):
        data = self.retriever.retrieve(user_query,name_space)
        response = self.generator.generate_response(user_query,data['fine'],data['medium'])
        return response