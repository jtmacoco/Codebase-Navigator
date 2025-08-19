from pydantic import BaseModel

class GitRepoReq(BaseModel):
    github_url: str
    branch: str | None = None

class ChatReq(BaseModel):
    message:str
    repo_name:str