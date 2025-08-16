from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import os
import json
config = load_dotenv(dotenv_path="./.backend_env")

pc = Pinecone(api_key=os.getenv("PINECONE"))
index_name = os.getenv("NAME")
tags = json.loads(os.getenv("TAGS"))
if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
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
pinecone_index = pc.Index(index_name)
def get_pinecone_index():
    return pinecone_index

def pincone_upsert_vectors(name_space:str,vectors:list):
    pinecone_index.upsert(
        namespace=name_space,
        vectors=vectors
    )

