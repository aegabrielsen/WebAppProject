import html
import uuid
from bson.objectid import ObjectId
from util.cookie_auth import *
from util.mongo import chat_collection
from util.multipart import parse_multipart

def media_uploads(request, handler):
    print(request.body)
    multipart = parse_multipart(request)
    # message_obj = json.loads(request.body)
    # sent_xsrf_token = message_obj["xsrf_token"]
    user_browser_id = request.cookies.get("user")
    user = cookie_auth(request)
    # invalid_user = False
    # multipart.parts[0] # Hardcoding it to assume the part at the 0th index is the image. Should be changed if feature is expanded
    image_id = str(uuid.uuid4())
    file = open(f"public/image/image{image_id}.jpg", "wb") #Hardcoding it to assume it is only getting jpgs
    file.write(multipart.parts[0].content)
    file.close()

    if user:
        # if user.get('xsrf_token') == sent_xsrf_token:
        chat_collection.insert_one({"username": user.get('username'), "message": f'<img src="public/image/image{image_id}.jpg">', "user_browser_id": user_browser_id})
        # else:
        #     invalid_user = True
    else:
        chat_collection.insert_one({"username": "Guest", "message": f'<img src="public/image/image{image_id}.jpg">', "user_browser_id": user_browser_id})
    # if invalid_user:
        # response = f"HTTP/1.1 403 Forbidden\r\nContent-Length: 0\r\nContent-Type: text/plain; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    # else:    
        # response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(text.encode())}\r\nContent-Type: text/plain; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n{text}"
    response = f"HTTP/1.1 302 Found\r\nContent-Length: 0\r\nContent-Type: text/html; charset=utf-8\r\nLocation: /\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    handler.request.sendall(response.encode())
