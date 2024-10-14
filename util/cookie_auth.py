import hashlib
from pymongo import MongoClient
mongo_client = MongoClient("mongo")
db = mongo_client["cse312"]
user_collection = db["users"]

def cookie_auth(request):
    auth_token = request.cookies.get("auth_token")
    if auth_token is None:
        return None
    auth_token = request.cookies.get("auth_token")
    hashed_auth_token = hashlib.sha256(auth_token.encode()).hexdigest()
    user = user_collection.find_one({"auth_token" : hashed_auth_token})
    if user is None:
        return None
    return user