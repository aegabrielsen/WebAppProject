from pymongo import MongoClient
import os
docker_db = os.environ.get("DOCKER_DB", "false")

if docker_db == "true":
    print("using docker compose db")
    mongo_client = MongoClient("mongo")
else:
    print("using local db")
    mongo_client = MongoClient("localhost")

db = mongo_client["cse312"]
chat_collection = db["chat"]
user_collection = db["users"]