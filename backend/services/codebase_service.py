from models.schemas import GitRepoReq
from services.parser import get_all_methods
from services.chunker import chunk_code
from services.embeddings_service import embed_chunks_batching
from services.repo_manager import clone_repo, parseUrl
class CodebaseService:
    def __init__(self,index):
        self.index = index

    def process_repo(self,payload:GitRepoReq):
        url = payload.github_url
        ssh_url,repo = parseUrl(url=url)
        with clone_repo(ssh_url,repo) as tmpdir:
            methods = get_all_methods(tmpdir)
            chunks = chunk_code(methods)
            embed_chunks_batching(chunks,repo)
        return {"success":"True","url":payload.github_url,"branch":payload.branch}