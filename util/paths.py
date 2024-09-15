
# response when a file doesn't exist
def error_404(request, handler):
    response = "HTTP/1.1 404 Not Found\r\nContent-Length: 36\r\nContent-Type: text/plain; charset=utf-8\r\n\r\nThe requested content does not exist"
    handler.request.sendall(response.encode())

# send home_page to /
def home_page(request, handler):
    response = "HTTP/1.1 200 OK\r\nContent-Length: 7\r\nContent-Type: text/plain; charset=utf-8\r\n\r\nWelcome"
    handler.request.sendall(response.encode())