from fastapi import HTTPException
from services.codebase_service import CodebaseService
from models.schemas import GitRepoReq
from errors.errors import InvalidUrl,CloneError, ProcessCodebaseError
class CodebaseController:
    def __init__(self,service):
        self.service = service
    def get_repo(self,payload:GitRepoReq):
        try:
            return self.service.process_repo(payload)
        except InvalidUrl as e:
            raise HTTPException(status_code=400,detail=str(e))
        except ProcessCodebaseError as e:
            raise HTTPException(status_code=400,detail=str(e))
        except CloneError as e:
            raise HTTPException(status_code=400,detail=str(e))

