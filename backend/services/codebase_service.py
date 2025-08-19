from models.schemas import GitRepoReq
from services.parser import get_all_methods, get_all_code
from services.chunker import chunk_code, chunk_file
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
            files = get_all_code(tmpdir)

            chunks = chunk_code(methods)
            file_chunks = chunk_file(files)

            embed_chunks_batching(file_chunks,repo,index=2)
            embed_chunks_batching(chunks,repo,index=1)
        return {"success":"True","repo_name":repo}