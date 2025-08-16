from urllib.parse import urlparse
from pathlib import Path
import tempfile
import subprocess
from contextlib import contextmanager
'''
Clones a github repository into a tmp directory

Args:
    ssh_url (String): ssh url
    repo_name (String): repo name

Returns:
    None
'''
@contextmanager
def clone_repo(ssh_url: str, repo_name:str):
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            cmd = ["git","clone"]
            cmd+=[ssh_url,tmpdir]
            subprocess.run(cmd,capture_output=True,text=True,check=True)
            yield tmpdir

            '''
            methods = self.get_all_methods(tmpdir)
            method_chunks = self.chunk_code(methods)
            methods_embed = self.embed_chunks_batching(method_chunks,repo_name)
            '''

        except subprocess.CalledProcessError as e:
            print(f"CLONE FAILED:{e}")
            raise

'''
Parses a url obtaining the ssh_url

Args:
    url (String): github url

Return:
    ssh_url (String): A string which is the ssh_url
    repo (String): A string which is the repository name
'''
def parseUrl(url:str):
    parsed = urlparse(url)
    parts = parsed.path.strip("/").split("/")
    owner,repo = parts[0],parts[1]
    ssh_url= f"git@github.com:{owner}/{repo}.git"
    return ssh_url,repo