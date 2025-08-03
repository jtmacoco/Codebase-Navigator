from services.codebase_service import CodebaseService
from models.schemas import GitRepoReq
class CodebaseController:
    def __init__(self):
        self.service = CodebaseService()
    def get_repo(self,payload:GitRepoReq):
        return self.service.process_repo(payload)
