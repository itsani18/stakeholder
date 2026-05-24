from pymongo import MongoClient

MONGO_URL = "mongodb://localhost:27017"

client = MongoClient(MONGO_URL)

database = client["stakeholder_db"]

raw_feedback_collection = database["raw_feedback"]

analysis_collection = database["analysis"]