from fastapi import APIRouter,status,Body
from typing import Annotated
from fastapi.responses import JSONResponse
from models.schemas import GitRepoReq
from controllers.codebase_ctrl import CodebaseController

router = APIRouter(prefix="/codebase",tags=["Codebase Assistant"])
controller = CodebaseController()
@router.post("/gitUrl")
def get_github_url(payload: Annotated[GitRepoReq,Body()]):
    res = controller.get_repo(payload)
    return JSONResponse(status_code=status.HTTP_200_OK, content=res)