import json
from pymongo import MongoClient
mongo_client = MongoClient("mongo")
db = mongo_client["cse312"]
chat_collection = db["chat"]

def chat_post(request, handler):
    text = "Message sent"
    print(request.body)
    message_obj = json.loads(request.body)
    chat_collection.insert_one({"username": "Guest", "message": message_obj["message"]})
    response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(text.encode())}\r\nContent-Type: text/plain; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n{text}"
    handler.request.sendall(response.encode())

def chat_get(request, handler):
    text = "Message received"
    print(request.body)
    response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(text.encode())}\r\nContent-Type: text/plain; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n{text}"
    handler.request.sendall(response.encode())