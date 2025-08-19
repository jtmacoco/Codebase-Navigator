from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import UpdateOne
from bson import ObjectId
from dotenv import load_dotenv
import os 
config = load_dotenv(dotenv_path="./.backend_env")
uri = os.getenv("DB_PATH")

client = MongoClient(uri, server_api=ServerApi('1'))
db = client[os.getenv("DB")]
collection = db[os.getenv("COLLECTION")]

def one_insert(doc:dict):
    collection.insert_one(doc)

def insert_many(many:list):
    operations = []
    for doc in many:
        operations.append(
            UpdateOne({"_id":doc["_id"]},{"$set":doc}, upsert=True)
        )
    collection.bulk_write(operations)
    #collection.insert_many(many)

def get_code_chunk(id:str):
    doc = collection.find_one({"_id":id})
    return doc