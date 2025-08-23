from embeddings.embedder import embed
from embeddings.pinecone_index import pincone_upsert_vectors
from concurrent.futures import ThreadPoolExecutor, as_completed
from mongo.mongodb_config import insert_many
import torch
import hashlib
'''
Generates a uid based on code_chunks

Args:
    repo_name (str): Repository name
    code_chunks (str): A single source code chunk

Returns
    str: A string combining the repo name with hashed code chunk
'''

def gen_id(repo_name:str,code_chunks:str):
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
def upsert_batch(all_embeddings:list,chunk_metadata:list,repo_name:str, code_data:list,index, batch_size=32):
    vectors_to_upsert = []
    futures = []
    chunk_code_data = []
    for (emb, meta,code) in zip(all_embeddings,chunk_metadata,code_data):
        idx = gen_id(repo_name,code)
        vectors_to_upsert.append({
            "id":idx,
            "values":emb,
            "metadata":meta
        })
        chunk_code_data.append({"_id":idx,"code":code})
    #UNCOMMENT WHEN WANT TO ACTUALLY EMBED, TRYING NOT TO WASTE FREE TIER LOL
    '''
    def insert_chunks():
        for i in range(0,len(chunk_code_data),batch_size):
            insert_many(chunk_code_data[i:i+batch_size])
    def upsert_vectors(): 
        for i in range(0,len(vectors_to_upsert),batch_size):
            pincone_upsert_vectors(name_space=repo_name,vectors=vectors_to_upsert[i:i+batch_size],index=index)
    with ThreadPoolExecutor() as executor:
        futures = [
        executor.submit(insert_chunks),
        executor.submit(upsert_vectors)
        ]
        for f in futures:
            f.result()
    '''
'''
Prepares code chunks and embeds code chunks in batches

Args:
    chunks (list): A list of code chunks
    repo_name: A string which is the repository name

Returns:
    None

'''
def embed_chunks_batching(chunks_with_meta:dict,repo_name:str,index=1):
    all_chunks = [f"File: {str(c["file"])}\n\n type:{c["type"]}\n\n ---\n\n"+c["code"] for c in chunks_with_meta]
    metadata = [
        {
            "repo": repo_name,
            "function_name": c["function_name"],
            "chunk_index": c["chunk_index"],
            "type":c["type"],
            "file":str(c["file"]),
            "file_path":c["file_path"],
        }
        for c in chunks_with_meta
    ]
    code_data = all_chunks[:]
    all_embeddings=embed(all_chunks)
    upsert_batch(all_embeddings,metadata,repo_name,code_data,index)
        