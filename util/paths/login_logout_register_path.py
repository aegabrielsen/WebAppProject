import bcrypt
import hashlib
import uuid
from util.auth import *
from util.cookie_auth import *
from pymongo import MongoClient
mongo_client = MongoClient("mongo")
db = mongo_client["cse312"]
user_collection = db["users"]

def login(request, handler):
    credentials = extract_credentials(request)
    username = credentials[0]
    password = credentials[1]
    auth_token = None

    user = user_collection.find_one({"username" : username})
    if user:
        salt = user.get('salt')
        correct_password = user.get('password')
        password = bcrypt.hashpw(password.encode(), salt)
        if password == correct_password:
            auth_token = str(uuid.uuid4())
            hashed_auth_token = hashlib.sha256(auth_token.encode()).hexdigest()
            # print(auth_token)
            # print(hashed_auth_token)
            user_collection.update_one({"username" : username}, {"$set" : {"auth_token" : hashed_auth_token}})

    if auth_token:
        response = f"HTTP/1.1 302 Found\r\nContent-Length: 0\r\nContent-Type: text/html; charset=utf-8\r\nLocation: /\r\nSet-Cookie: auth_token={auth_token}; Max-Age=360000; HttpOnly\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    else:
        response = f"HTTP/1.1 302 Found\r\nContent-Length: 0\r\nContent-Type: text/html; charset=utf-8\r\nLocation: /\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    handler.request.sendall(response.encode())


def register(request, handler):
    credentials = extract_credentials(request)
    username = credentials[0]
    password = credentials[1]
    if (validate_password(password)):
        # hash password
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(password.encode(), salt)
        user = user_collection.find_one({"username" : username})
        if user == None: # If there is no user associated with the given username
            user_collection.insert_one({"username": username, "password": password, "salt": salt})
        else:
            print("User already exists")
    else:
        print("Invalid password")

    response = f"HTTP/1.1 302 Found\r\nContent-Length: 0\r\nContent-Type: text/html; charset=utf-8\r\nLocation: /\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    handler.request.sendall(response.encode())

def logout(request, handler):
    user = cookie_auth(request)
    if user:
        user_collection.update_one({ "username": user.get('username')}, {"$unset": {"auth_token": ""}})
    response = f"HTTP/1.1 302 Found\r\nContent-Length: 0\r\nContent-Type: text/html; charset=utf-8\r\nLocation: /\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    handler.request.sendall(response.encode())    