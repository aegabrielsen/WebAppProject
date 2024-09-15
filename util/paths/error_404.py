# response when a file doesn't exist
def error_404(request, handler):
    text = "The requested content does not exist"
    response = f"HTTP/1.1 404 Not Found\r\nContent-Length: {len(text.encode())}\r\nContent-Type: text/plain; charset=utf-8\r\n\r\n{text}"
    handler.request.sendall(response.encode())