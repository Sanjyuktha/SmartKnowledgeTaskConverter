import os
from pymongo import MongoClient

# 1. Safely look up the variable name we will give to Streamlit Cloud
mongo_uri = os.getenv("mongodb+srv://sanjyukthad2024it_db_user:suns09@cluster0.ddrvj4p.mongodb.net/?appName=Cluster0")

# 2. Pass that correct variable name directly into the client
client = MongoClient(mongo_uri)

db = client["SmartKnowledgeDB"]
collection = db["projects"]
