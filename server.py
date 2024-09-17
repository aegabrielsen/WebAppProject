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
        # TODO: Add your routes here
        super().__init__(request, client_address, server)

    def handle(self):
        received_data = self.request.recv(2048)
        print(self.client_address)
        print("--- received data ---")
        print(received_data)
        print("--- end of data ---\n\n")
        request = Request(received_data)

        self.router.route_request(request, self)


def main():
    host = "0.0.0.0"
    port = 8080
    socketserver.TCPServer.allow_reuse_address = True

    server = socketserver.TCPServer((host, port), MyTCPHandler)

    print("Listening on port " + str(port))
    server.serve_forever()


if __name__ == "__main__":
    main()
