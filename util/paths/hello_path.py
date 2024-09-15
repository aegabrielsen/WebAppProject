
# This path is provided as an example of how to use the router
def hello_path(request, handler):
    text = "hello"
    response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(text.encode())}\r\nContent-Type: text/plain; charset=utf-8\r\n\r\n{text}"
    handler.request.sendall(response.encode())