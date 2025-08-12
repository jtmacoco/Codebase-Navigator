from models.schemas import ChatReq
from services.chat_service import ChatService
class ChatController():
    def __init__(self,index):
        self.index = index
        self.service = ChatService(self.index)

    def post_message(self,payload:ChatReq):
        return self.service.process_message(payload)
