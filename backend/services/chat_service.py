from models.schemas import ChatReq
from rag.pipeline import RAGPipeline 

class ChatService:
    def __init__(self,index):
        self.index = index
        self.pipeline = RAGPipeline()
    def process_message(self,payload:ChatReq):
        response = self.pipeline.query(payload.message,payload.repo_name)
        #print(payload.message,payload.repo_name)
        return {"response":response}