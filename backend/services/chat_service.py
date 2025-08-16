from models.schemas import ChatReq

class ChatService:
    def __init__(self,index):
        self.index = index
    def process_message(self,payload:ChatReq):
        return {"message":payload.message} 