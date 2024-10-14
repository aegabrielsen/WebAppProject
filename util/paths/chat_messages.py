import json
import html
from pymongo import MongoClient
from bson.objectid import ObjectId
from util.cookie_auth import *
mongo_client = MongoClient("mongo")
db = mongo_client["cse312"]
chat_collection = db["chat"]
user_collection = db["users"]

def chat_post(request, handler):
    text = "Message sent"
    print(request.body)
    message_obj = json.loads(request.body)
    sent_xsrf_token = message_obj["xsrf_token"]
    user_browser_id = request.cookies.get("user")
    user = cookie_auth(request)
    invalid_user = False
    if user:
        if user.get('xsrf_token') == sent_xsrf_token:
            chat_collection.insert_one({"username": user.get('username'), "message": html.escape(message_obj["message"]), "user_browser_id": user_browser_id})
        else:
            invalid_user = True
    else:
        chat_collection.insert_one({"username": "Guest", "message": html.escape(message_obj["message"]), "user_browser_id": user_browser_id})
    if invalid_user:
        response = f"HTTP/1.1 403 Forbidden\r\nContent-Length: 0\r\nContent-Type: text/plain; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    else:    
        response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(text.encode())}\r\nContent-Type: text/plain; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n{text}"
    handler.request.sendall(response.encode())

def chat_get(request, handler):
    chats = list(chat_collection.find())
    # print(chats)
    for i in chats:
        i['id'] = str(i.pop("_id"))
    # print(chats)
    
    chat_history = json.dumps(chats)
    response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(chat_history)}\r\nContent-Type: text/plain; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n{chat_history}"
    handler.request.sendall(response.encode())

def chat_delete(request, handler):
    # print(request)
    # print(request.path)
    # print(request.body)
    user = cookie_auth(request)
    chat_id  = ObjectId(request.path.replace('/chat-messages/', ''))
    
    chat = chat_collection.find_one({"_id" : chat_id})
    if chat_id and user and chat.get('username') == user.get('username'):
        chat_collection.delete_one({'_id': chat_id})
        response = f"HTTP/1.1 204 No Content\r\nContent-Length: 0\r\nContent-Type: text/plain; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    else:
        response = f"HTTP/1.1 403 Forbidden\r\nContent-Length: 0\r\nContent-Type: text/plain; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    handler.request.sendall(response.encode())