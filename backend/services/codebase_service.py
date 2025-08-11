from models.schemas import GitRepoReq
from urllib.parse import urlparse
from tree_sitter import Language, Parser
from pathlib import Path
from tree_sitter_language_pack import get_language, get_parser
from constants.languages import LANGUAGES
from embeddings.embedder import embed
from embeddings.pinecone_index import pincone_upsert_vectors
import tempfile
import subprocess
class CodebaseService:
    def __init__(self,index):
        self.index = index
    '''
    - Description:
        - Finds all functions within a file
    - Args: 
        - source_code (String): All of the source code
        - parser (Parser): A tree_sitter parser
    - Return:
        - list of functions and function names
    '''
    def get_functions(self,source_code:str,parser:Parser):
        tree = parser.parse(bytes(source_code,'utf8'))
        root = tree.root_node
        def find_name(node):
            name_node = node.child_by_field_name("name")
            if name_node:
                return source_code[name_node.start_byte:name_node.end_byte]
            for child in node.children:
                if child.type == 'identifier':
                    return source_code[child.start_byte:child.end_byte]
                found = find_name(child)
                if found:
                    return found
            return None
        def recurse(node):
            if node.type in ('function_definition', 'method_definition'):
                func_name=find_name(node)
                yield {"node":node,"name":func_name}
            for child in node.children:
                yield from recurse(child)
        return list(recurse(root))
    
    '''
    - Description:
        - Separates code chunks by functions and upsert's data into pinecone
    - Args:
        - file_path (String): path to file
    '''
    def chunk_code(self,file_path:str,repo_name:str):
        path = Path(file_path)
        parsers = {}
        vectors = []
        vec_id_counter = 0
        #loop grabs all the parsers for every Language in LANGUAGES
        for ext,lang_name in LANGUAGES.items():
            lang = get_language(lang_name)
            parser = Parser(lang)
            parsers[ext] = parser

        for file_path in path.rglob("*"):
            if file_path.is_file() and file_path.suffix in LANGUAGES.keys():
                parser = parsers[file_path.suffix]
                try:
                    with open(file_path,'r',encoding='utf-8') as f:
                        content = f.read()
                        functions = self.get_functions(content,parser)
                        for func_node in functions:
                            func_code = content.encode('utf-8')[func_node["node"].start_byte:func_node["node"].end_byte].decode('utf-8')
                            result = embed(code_chunks=func_code)
                            vectors.append({
                                "id":f"vec-{vec_id_counter}",
                                "values":result,
                                "metadata":{
                                    "function_name":str(func_node["name"]),
                                    "file_path":str(file_path)
                                }
                            })
                            vec_id_counter+=1
                        
                        tree = parser.parse(bytes(content,'utf8'))
                        #print(f"Parsed {file_path} successfully")
                except Exception as e:
                    print(f"ERROR READING {file_path}:{e}")
        #uncomment when doing more testing for backend, so don't use up all free tier
        #pincone_upsert_vectors(name_space=repo_name,vectors=vectors)
         
    '''
    - Description:
        - Clones a repo in temp directory
    - Args:
        - ssh_url (String): ssh url
        - repo_name (String): repo name
    '''
    def clone_repo(self,ssh_url: str, repo_name:str):
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                cmd = ["git","clone"]
                cmd+=[ssh_url,tmpdir]
                subprocess.run(cmd,capture_output=True,text=True,check=True)
                self.chunk_code(tmpdir,repo_name)
            except subprocess.CalledProcessError as e:
                print(f"CLONE FAILED:{e}")
                raise
    '''
    - Description:
        - Parses url obtaining ssh url
    - Args:
        - url (String): github url
    - Return:
        - ssh_url (String): ssh url
        - repo (String): repo name
    '''
    def parseUrl(self,url:str):
        parsed = urlparse(url)
        parts = parsed.path.strip("/").split("/")
        owner,repo = parts[0],parts[1]
        ssh_url= f"git@github.com:{owner}/{repo}.git"
        return ssh_url,repo

    def process_repo(self,payload:GitRepoReq):
        url = payload.github_url
        ssh_url,repo = self.parseUrl(url)
        self.clone_repo(ssh_url=ssh_url,repo_name=repo)
        return {"success":"True","url":payload.github_url,"branch":payload.branch}