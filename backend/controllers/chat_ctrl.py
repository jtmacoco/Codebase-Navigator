from models.schemas import ChatReq
from fastapi import HTTPException
from services.chat_service import ChatService
from errors.errors import RAGError
class ChatController():
    def __init__(self,index):
        self.index = index
        self.service = ChatService(self.index)

    def post_message(self,payload:ChatReq):
        try:
            return self.service.process_message(payload)
        except RAGError as e:
            raise HTTPException(status_code=400,detail=str(e))
