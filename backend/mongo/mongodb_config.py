from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os 
config = load_dotenv(dotenv_path="./.backend_env")
uri = os.getenv("DB_PATH")

client = MongoClient(uri, server_api=ServerApi('1'))
db = client[os.getenv("DB")]
collection = db[os.getenv("COLLECTION")]
doc = {"name":"test"}

def one_insert(doc:dict):
    collection.insert_one(doc)

def insert_many(many:list):
    collection.insert_many(many)
