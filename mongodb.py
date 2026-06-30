import os
from pymongo import MongoClient

# 1. Safely look up the variable name we will give to Streamlit Cloud
mongo_uri = os.getenv("MONGO_URI")
# 2. Pass that correct variable name directly into the client
client = MongoClient(mongo_uri)

db = client["SmartKnowledgeDB"]
collection = db["projects"]
