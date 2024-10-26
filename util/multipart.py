from util.request import Request

def parse_multipart(Request: Request):
    return Multipart_Request()


class Multipart_Request:
    def __init__(self, boundary, parts):
        self.boundary = boundary
        self.parts = parts
        
class Part:
    def __init__(self, headers, name, content: bytes):
        self.headers = headers
        self.name = name
        self.content = content