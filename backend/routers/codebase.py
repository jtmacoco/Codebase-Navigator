from fastapi import APIRouter,status,Body
from typing import Annotated
from fastapi.responses import JSONResponse
from models.schemas import GitRepoReq
from controllers.codebase_ctrl import CodebaseController
from services.codebase_service import CodebaseService
from embeddings.pinecone_index import get_pinecone_index

def codebase_router():
    router = APIRouter(prefix="/codebase",tags=["Codebase Assistant"])
    pc_index = get_pinecone_index()
    codebase_service = CodebaseService(pc_index)
    codebase_ctrl = CodebaseController(codebase_service)

    @router.post("/gitUrl")
    def get_github_url(payload: Annotated[GitRepoReq,Body()]):
        res = codebase_ctrl.get_repo(payload)
        return JSONResponse(status_code=status.HTTP_200_OK, content=res)
    return router