from models.schemas import GitRepoReq
from urllib.parse import urlparse
from tree_sitter import Language, Parser
from pathlib import Path
from tree_sitter_language_pack import get_language, get_parser
from constants.languages import LANGUAGES
from constants.methods import ALL_METHODS, FILTER_METHODS
from embeddings.embedder import embed
from embeddings.pinecone_index import pincone_upsert_vectors
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import chain
from mongo.mongodb_config import insert_many
from aws.aws_config import get_file, put_chunks
import torch
import time
import hashlib
import tempfile
import subprocess
class CodebaseService:
    def __init__(self,index):
        self.index = index
    
    '''
    Filters methods if total number of methods is greater thanmax_size

    Args:
        all_methods (dict): A dict mapping methods names to their data
                            where each value is a dict with "type" and "code" keys
        max_size (optional): Max number of methods to keep before filtering, defaults to 5,000

    Returns:
        dict[str,str]: A dict mapping method names to their code only, excluding method and other,
                       metadata
    '''
    def filter_methods(self,all_methods:dict,max_size=5000):
        if len(all_methods)>max_size:
            allowed_types = FILTER_METHODS
            all_methods = {
                name: data 
                for name, data in all_methods.items()
                if data["type"] in allowed_types
            }
        return{name:data["code"] for name,data in all_methods.items()}
    
    '''
    Extracts the source code methods from a github repo, using Tree-sitter parser

    Args:
        source_code (str): The source code for that file
        parser (Parser): The specific parser needed to parse the file (using tree-sitter)

    Returns:
        list[dict]: A list of dictionaries each containing:
            "node": the Tree-sitter node of the method
            "name": the name of the method as a string
    '''
    def get_code_methods(self,source_code:str,parser:Parser):
        tree = parser.parse(bytes(source_code,'utf8'))
        root = tree.root_node
        target_type = ALL_METHODS

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
            return ""
        def recurse(node):
            if node.type in target_type:
                func_name=find_name(node)
                yield {"node":node,"name":func_name}
            for child in node.children:
                yield from recurse(child)
        return list(recurse(root))
    '''
    Extract all the methods from a file

    This function recursivley scans a file and parses the file using a language-specific
    parsers (Tree-sitter) and collects all the methods

    Args:
        file_path (str): Path to the file to scan

    Returns:
        dict[str,str]: A dict mapping method names to their code 
    '''
    def get_all_methods(self,file_path:str):
        path = Path(file_path)
        parsers = {}
        all_methods= {}
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
                    methods = self.get_code_methods(content,parser)
                    for method_node in methods:
                        method_code = content.encode('utf-8')[method_node["node"].start_byte:method_node["node"].end_byte].decode('utf-8')
                        method_name = str(method_node["name"])
                        #all_methods[method_name] = str(method_code)
                        all_methods[method_name] = {
                            "code":method_code,
                            "type":method_node["node"].type
                        }
                    tree = parser.parse(bytes(content,'utf8'))
                except Exception as e:
                    print(f"ERROR READING {file_path}:{e}")
        all_methods=self.filter_methods(all_methods)
        return all_methods
    
    '''
    Generates a uid based on code_chunks

    Args:
        repo_name (str): Repository name
        code_chunks (str): A single source code chunk
    
    Returns
        str: A string combining the repo name with hashed code chunk
    '''

    def gen_id(self,repo_name:str,code_chunks:str):
        chunk_hash = hashlib.sha256(code_chunks.encode("utf-8")).hexdigest()[:16]
        return f"{repo_name}-{chunk_hash}"

    '''
    Perpare and insert data into MongoDB and Pinecone in batches

    Args:
        all_embeddings (list): A list containing all the embedding vectors
        chunk_metadata (list): A list containing all of the meta data for all code chunks
        code_data (list): A list containing all of the code chunks
        batch_size (int, optional): An int setting the batch size
    
    Returns:
      None

    '''
    def upsert_batch(self,all_embeddings:list,chunk_metadata:list,repo_name:str, code_data:list, batch_size=32):
        vectors_to_upsert = []
        futures = []
        chunk_code_data = []
        for (emb, meta,code) in zip(all_embeddings,chunk_metadata,code_data):
            idx = self.gen_id(repo_name,code)
            vectors_to_upsert.append({
                "id":idx,
                "values":emb,
                "metadata":meta
            })
            chunk_code_data.append({"_id":idx,"code":code})
        '''
        UNCOMMENT WHEN WANT TO ACTUALLY EMBED, TRYING NOT TO WASTE FREE TIER LOL
        def insert_chunks():
            for i in range(0,len(chunk_code_data),batch_size):
                insert_many(chunk_code_data[i:i+batch_size])
        def upsert_vectors(): 
            for i in range(0,len(vectors_to_upsert),batch_size):
                pincone_upsert_vectors(name_space=repo_name,vectors=vectors_to_upsert[i:i+batch_size])
        with ThreadPoolExecutor() as executor:
            executor.submit(insert_chunks)
            executor.submit(upsert_vectors)
        '''

    '''
    Prepares code chunks and embeds code chunks in batches

    Args:
        chunks (list): A list of code chunks
        repo_name: A string which is the repository name
    
    Returns:
        None

    '''
    def embed_chunks_batching(self,chunks:list,repo_name:str):
        all_chunks = []
        chunk_metadata = []
        code_data = []
        for func_name, chunk_list in chunks.items():
            for idx, chunk_text in enumerate(chunk_list):
                all_chunks.append(chunk_text)
                chunk_metadata.append({
                    "function_name":func_name,
                    "chunk_index":idx,
                })
                code_data.append(chunk_text)
        
        all_embeddings = embed(all_chunks)
        '''
        use for comparing parallel to non-parallel
        all_embeddings = []
        batches = [all_chunks[i:i+batch_size] for i in range(0,len(all_chunks),batch_size) if all_chunks[i:i+batch_size]]
        all_embeddings=[embed(batch) for batch in batches]
        all_embeddings=torch.cat(all_embeddings,dim=0)
        all_embeddings=all_embeddings.tolist()
        '''
        self.upsert_batch(all_embeddings,chunk_metadata,repo_name,code_data)

    ''' 
    Split function code into smaller chunks based on byte size

    Args:
        functions (dict): A dictionary containing the function names to their code
        max_bytes (int, optional): Max size in bytes for each chunk. Default value 30,000

    Returns:
        dict[str,list[str]]: Dic mapping functions names to list of code chunks
    ''' 
    def chunk_code(self,functions:dict,max_bytes=30_000):
        chunks = defaultdict(list)
        for name, code in functions.items():
            current_chunk = []
            current_size = 0
            chunk_id = 0
            for line in code.splitlines(keepends=True):
                line_bytes = (len(line.encode('utf-8')))
                if current_size + line_bytes > max_bytes:
                    chunks[name].append("".join(current_chunk))
                    current_chunk = [line]
                    current_size = line_bytes
                else:
                    current_chunk.append(line)
                    current_size += line_bytes
            if current_chunk:
                chunks[name].append("".join(current_chunk))
        return chunks
    
         
    '''
    Clones a github repository into a tmp directory

    Args:
        ssh_url (String): ssh url
        repo_name (String): repo name

    Returns:
      None
    '''
    def clone_repo(self,ssh_url: str, repo_name:str):
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                cmd = ["git","clone"]
                cmd+=[ssh_url,tmpdir]
                subprocess.run(cmd,capture_output=True,text=True,check=True)

                methods = self.get_all_methods(tmpdir)
                method_chunks = self.chunk_code(methods)
                methods_embed = self.embed_chunks_batching(method_chunks,repo_name)

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