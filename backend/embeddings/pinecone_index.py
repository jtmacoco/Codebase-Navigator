from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import os
import json
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

def pinecone_retriever(namespace:str,user_query):
    result_fine = pinecone_index_fine.query(
        namespace=namespace,
        vector=user_query,
        top_k=2,
        include_metadata=True
    )
    result_medium = pinecone_index_medium.query(
        namespace=namespace,
        vector=user_query,
        top_k=2,
        include_metadata=True
    )
    return result_fine,result_medium