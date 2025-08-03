from pydantic import BaseModel

class GitRepoReq(BaseModel):
    github_url: str
    branch: str | None = None
