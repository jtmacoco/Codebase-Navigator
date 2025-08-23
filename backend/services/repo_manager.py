from urllib.parse import urlparse
from pathlib import Path
import tempfile
import subprocess
from contextlib import contextmanager
from errors.errors import InvalidUrl,CloneError
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

        except subprocess.CalledProcessError as e:
            raise CloneError

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
    if len(parts)<2:
        raise InvalidUrl
    owner,repo = parts[0],parts[1]
    ssh_url= f"git@github.com:{owner}/{repo}.git"
    return ssh_url,repo