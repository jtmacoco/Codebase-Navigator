from models.schemas import GitRepoReq
class CodebaseService:
    def process_repo(self,payload:GitRepoReq):
        return {"sucess":"True","url":payload.github_url,"branch":payload.branch}
        pass