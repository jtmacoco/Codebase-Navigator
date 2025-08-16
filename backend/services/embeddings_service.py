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
def upsert_batch(all_embeddings:list,chunk_metadata:list,repo_name:str, code_data:list, batch_size=32):
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
    '''
    #UNCOMMENT WHEN WANT TO ACTUALLY EMBED, TRYING NOT TO WASTE FREE TIER LOL
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
def embed_chunks_batching(chunks:list,repo_name:str):
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
    upsert_batch(all_embeddings,chunk_metadata,repo_name,code_data)
        