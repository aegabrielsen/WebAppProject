def chat_post(request, handler):
    text = "Message sent"
    print(request.body)
    response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(text.encode())}\r\nContent-Type: text/plain; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n{text}"
    handler.request.sendall(response.encode())

def chat_get(request, handler):
    text = "Message received"
    print(request.body)
    response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(text.encode())}\r\nContent-Type: text/plain; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n{text}"
    handler.request.sendall(response.encode())