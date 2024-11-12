from util.read_frames import while_reading_frames
from util.websockets import compute_accept
def websocket_path(request, handler):
    print(request.headers)
    print(request.body)
    accept = compute_accept(request.headers.get('Sec-WebSocket-Key', 0))
    response = f"HTTP/1.1 101 Switching Protocols\r\nContent-Length: 0\r\nConnection: Upgrade\r\nUpgrade: websocket\r\nSec-WebSocket-Accept: {accept}\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    handler.request.sendall(response.encode())
    while_reading_frames(request, handler)