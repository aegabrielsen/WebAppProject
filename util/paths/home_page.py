# send home_page to /
def home_page(request, handler):
    f = open("public/index.html", "rb")
    index = f.read().decode()
    visits = int(request.cookies.get("visits", 0)) + 1
    index = index.replace("{{visits}}", str(visits))
    index = index.encode()
    response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(index)}\r\nContent-Type: text/html; charset=utf-8\r\nSet-Cookie: visits={visits}; Max-Age=3600\r\nX-Content-Type-Options: nosniff\r\n\r\n{index.decode()}"
    handler.request.sendall(response.encode())