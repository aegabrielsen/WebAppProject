import uuid
import os
import json
import hashlib
import requests
import base64
# from pymongo import MongoClient
# from bson.objectid import ObjectId
from util.cookie_auth import *
# mongo_client = MongoClient("mongo")
# db = mongo_client["cse312"]
# user_collection = db["users"]
from util.mongo import user_collection
# from server import user_collection
client_id = os.environ.get('CLIENT_ID', 'No variable')
client_secret = os.environ.get('CLIENT_SECRET', 'No variable')
redirect_uri = os.environ.get('REDIRECT_URI', 'No variable')
scope = 'user-read-email'

def spotify_login(request, handler):
    location = f"https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"
    response = f"HTTP/1.1 302 Found\r\nContent-Length: 0\r\nContent-Type: text/html; charset=utf-8\r\nLocation: {location}\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    handler.request.sendall(response.encode())


def spotify(request, handler):
    print('in /spotify')
    print(request.path)
    code = request.path.split('=')[1]
    print(code)
    
    response1 = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "code": code,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        },
        headers={
            "content-type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {base64.b64encode((f'{client_id}:{client_secret}'.encode())).decode()}"
        }
    )

    access_token = response1.json()["access_token"]

    response2 = requests.get(
        "https://api.spotify.com/v1/me",
        headers={
            "content-type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {access_token}"
        }
    )
    
    email = response2.json()["email"]
    user = user_collection.find_one({"username" : email})
    if user == None: # If there is no user associated with the given username
        user_collection.insert_one({"username": email})
    auth_token = str(uuid.uuid4())
    hashed_auth_token = hashlib.sha256(auth_token.encode()).hexdigest()
    user_collection.update_one({"username" : email}, {"$set" : {"auth_token" : hashed_auth_token}})

    response = f"HTTP/1.1 302 Found\r\nContent-Length: 0\r\nContent-Type: text/html; charset=utf-8\r\nLocation: /\r\nSet-Cookie: auth_token={auth_token}; Max-Age=360000; HttpOnly\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    handler.request.sendall(response.encode())