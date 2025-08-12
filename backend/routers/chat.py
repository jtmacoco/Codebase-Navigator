from fastapi import APIRouter,status,Body
from typing import Annotated
from fastapi.responses import JSONResponse
from models.schemas import ChatReq
from controllers.chat_ctrl import ChatController
from services.chat_service import ChatService
from embeddings.pinecone_index import get_pinecone_index

def chat_router():
    router = APIRouter(prefix="/api",tags=["Codebase Assistant"])
    pc_index = get_pinecone_index()
    chat_service = ChatService(pc_index)
    codebase_ctrl = ChatController(chat_service)
    
    @router.post("/chat")
    def post_message(payload: Annotated[ChatReq,Body()]):
        res = codebase_ctrl.post_message(payload)
        return JSONResponse(status_code=status.HTTP_200_OK, content=res)

    return router


