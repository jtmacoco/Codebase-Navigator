from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import os
import json
from rag.filterQuery import filter_query
config = load_dotenv(dotenv_path="./.backend_env")

pc1 = Pinecone(api_key=os.getenv("PINECONE"))
index_name_fine = os.getenv("NAME_1")
tags = json.loads(os.getenv("TAGS"))
if not pc1.has_index(index_name_fine):
    pc1.create_index(
        name=index_name_fine,
        vector_type=os.getenv("VECTOR_TYPE"),
        dimension=int(os.getenv("DIMENSION")),
        metric=os.getenv("METRIC"),
        spec=ServerlessSpec(
            cloud=os.getenv("CLOUD"),
            region=os.getenv("REGION")
        ),
        deletion_protection=os.getenv("DELETION"),
        tags=tags
    )

pc2 = Pinecone(api_key=os.getenv("PINECONE"))
index_name_medium = os.getenv("NAME_2")
tags = json.loads(os.getenv("TAGS"))
if not pc2.has_index(index_name_medium):
    pc2.create_index(
        name=index_name_medium,
        vector_type=os.getenv("VECTOR_TYPE"),
        dimension=int(os.getenv("DIMENSION")),
        metric=os.getenv("METRIC"),
        spec=ServerlessSpec(
            cloud=os.getenv("CLOUD"),
            region=os.getenv("REGION")
        ),
        deletion_protection=os.getenv("DELETION"),
        tags=tags
    )
pinecone_index_fine = pc1.Index(index_name_fine)
pinecone_index_medium = pc2.Index(index_name_medium)
def get_pinecone_index():
    return pinecone_index_fine

def pincone_upsert_vectors(name_space:str,vectors:list,index):
    if index == 1:
        pinecone_index_fine.upsert(
            namespace=name_space,
            vectors=vectors
        )
    elif index == 2:
        result = pinecone_index_medium.upsert(
            namespace=name_space,
            vectors=vectors
        )

def pinecone_retriever(namespace:str,embeded_query:list,user_query:str):
    filter_parms = filter_query(user_query)
    def query_index(index,apply_filter=False):
        return index.query(
        namespace=namespace,
        vector=embeded_query,
        top_k=2,
        include_metadata=True,
        filter=filter_parms if apply_filter else None
        )
    result_fine = query_index(pinecone_index_fine,apply_filter=True)
    result_medium= query_index(pinecone_index_medium,apply_filter=True)
    if not result_fine['matches']:
        result_fine = query_index(pinecone_index_fine,apply_filter=False)
    if not result_medium['matches']:
        result_medium = query_index(pinecone_index_medium,apply_filter=False)
    return result_fine,result_medium