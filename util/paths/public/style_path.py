# send style.css
def style_path(request, handler):
    f = open("public/style.css", "rb")
    file_contents = f.read()
    response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(file_contents)}\r\nContent-Type: text/css; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n{file_contents.decode()}"
    handler.request.sendall(response.encode())