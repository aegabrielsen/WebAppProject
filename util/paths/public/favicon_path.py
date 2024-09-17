# send favicon.ico
def favicon_path(request, handler):
    f = open("public/favicon.ico", "rb")
    file_contents = f.read()
    response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(file_contents)}\r\nContent-Type: image/vnd.microsoft.icon; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    response = response.encode() + file_contents
    handler.request.sendall(response)