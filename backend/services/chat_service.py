from models.schemas import ChatReq
from rag.pipeline import RAGPipeline 
from errors.errors import RAGError

class ChatService:
    def __init__(self,index):
        self.index = index
        self.pipeline = RAGPipeline()
    def process_message(self,payload:ChatReq):
        try:
            response = self.pipeline.query(payload.message,payload.repo_name)
        except Exception as e:
            raise RAGError
        return {"response":response}