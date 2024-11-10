import socketserver
from util.request import Request
from util.router import Router
from util.paths.hello_path import hello_path
from util.paths.home_page import home_page
from util.paths.public.favicon_path import favicon_path
from util.paths.public.functions_path import functions_path
from util.paths.public.image_paths import *
from util.paths.public.style_path import style_path
from util.paths.public.webrtc_path import webrtc_path
from util.paths.chat_messages import *
from util.paths.media_uploads import *
from util.paths.login_logout_register_path import *
from util.paths.spotify import *
from util.auth import *
from util.websockets import websocket_path
# from util.mongo import user_collection
# from util.mongo import chat_collection
# from pymongo import MongoClient
# mongo_client = MongoClient("mongo")
# db = mongo_client["cse312"]
# chat_collection = db["chat"]
# user_collection = db["users"]
# chat_collection.insert_one({"username": "hartloff", "message": "hello"})
class MyTCPHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.router = Router()
        self.router.add_route("GET", "/hello", hello_path, True)
        self.router.add_route("GET", "/", home_page, True)
        self.router.add_route("GET", "/favicon.ico", favicon_path, True)
        self.router.add_route("GET", "/public/favicon.ico", favicon_path, True)
        self.router.add_route("GET", "/public/style.css", style_path, True)
        self.router.add_route("GET", "/public/webrtc.js", webrtc_path, True)
        self.router.add_route("GET", "/public/functions.js", functions_path, True)
        self.router.add_route("GET", "/public/image/cat.jpg", cat_path, True)
        self.router.add_route("GET", "/public/image/dog.jpg", dog_path, True)
        self.router.add_route("GET", "/public/image/eagle.jpg", eagle_path, True)
        self.router.add_route("GET", "/public/image/elephant-small.jpg", elephant_small_path, True)
        self.router.add_route("GET", "/public/image/elephant.jpg", elephant_path, True)
        self.router.add_route("GET", "/public/image/flamingo.jpg", flamingo_path, True)
        self.router.add_route("GET", "/public/image/kitten.jpg", kitten_path, True)
        self.router.add_route("GET", "/public/image", uploaded_image, False)
        self.router.add_route("GET", "/chat-messages", chat_get, True)
        self.router.add_route("POST", "/chat-messages", chat_post, True)
        self.router.add_route("DELETE", "/chat-messages", chat_delete, False)
        self.router.add_route("POST", "/media-uploads", media_uploads, True)
        self.router.add_route("GET", "/websocket", websocket_path, True)

        self.router.add_route("POST", "/login", login, True)
        self.router.add_route("POST", "/register", register, True)
        self.router.add_route("POST", "/logout", logout, True)
        self.router.add_route("GET", "/spotify-login?", spotify_login, True)
        self.router.add_route("GET", "/spotify", spotify, False)
        # TODO: Add your routes here
        super().__init__(request, client_address, server)

    def handle(self):
        while True:
            received_data = self.request.recv(2048)
            print(self.client_address)
            print("--- received data ---")
            print(received_data)
            print("--- end of data ---\n\n")
            # print(chat_collection.find({"username": "hartloff"})[0])
            request = Request(received_data)
            # if 'Content-Length' in request.headers:
            content_length = int(request.headers.get('Content-Length', 0))
            received_body_length = len(request.body)
            while received_body_length < content_length:
                received_data_temp = self.request.recv(2048)
                received_data += received_data_temp
                received_body_length += len(received_data_temp)
            request = Request(received_data)
            self.router.route_request(request, self)





def main():
    host = "0.0.0.0"
    port = 8080
    socketserver.TCPServer.allow_reuse_address = True
    
    server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)

    print("Listening on port " + str(port))
    server.serve_forever()


if __name__ == "__main__":
    main()
