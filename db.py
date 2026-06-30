import os
from pymongo import MongoClient

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)

db = client["SmartKnowledgeDB"]

# Make sure this variable name matches exactly what app.py wants to import!
tasks_collection = db["projects"]
