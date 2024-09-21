import json
import html
from pymongo import MongoClient
from bson.objectid import ObjectId
mongo_client = MongoClient("mongo")
db = mongo_client["cse312"]
chat_collection = db["chat"]

def chat_post(request, handler):
    text = "Message sent"
    print(request.body)
    message_obj = json.loads(request.body)
    # "id": str(uuid.uuid4()), 
    chat_collection.insert_one({"username": "Guest", "message": html.escape(message_obj["message"])})
    response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(text.encode())}\r\nContent-Type: text/plain; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n{text}"
    handler.request.sendall(response.encode())

def chat_get(request, handler):
    chats = list(chat_collection.find())
    # print(chats)
    for i in chats:
        i['id'] = str(i.pop("_id"))
    print(chats)
    
    chat_history = json.dumps(chats)
    response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(chat_history)}\r\nContent-Type: text/plain; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n{chat_history}"
    handler.request.sendall(response.encode())

def chat_delete(request, handler):
    print(request)
    print(request.path)
    print(request.body)
    chat_collection.delete_one({'_id': ObjectId(request.path.replace('/chat-messages/', ''))})
    response = f"HTTP/1.1 204 No Content\r\nContent-Type: text/plain; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    handler.request.sendall(response.encode())