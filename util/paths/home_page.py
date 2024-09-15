# send home_page to /
def home_page(request, handler):
    f = open("public/index.html", "rb")
    index = f.read()
    response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(index)}\r\nContent-Type: text/html; charset=utf-8\r\n\r\n{index.decode()}"
    handler.request.sendall(response.encode())