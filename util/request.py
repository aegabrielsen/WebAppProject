class Request:

    def __init__(self, request: bytes):        
        self.body = b""
        self.method = ""
        self.path = ""
        self.http_version = ""
        self.headers = {} # Note: The raw Cookies header should still be in your headers dictionary even after parsing the individual cookies in the cookies dictionary. -a
        self.cookies = {} 

        body_line = request.split(b'\r\n\r\n')
        self.body = body_line[1]
        lines = body_line[0].split(b'\r\n')
        status_line = lines.pop(0).split(b' ') # No error checking. Consider checking if length != 3
        self.method = status_line[0].decode()
        self.path = status_line[1].decode()
        self.http_version = status_line[2].decode()

        for l in lines:
            header = l.decode().split(':', 1)
            self.headers[header[0]] = header[1].strip()
            # TODO: CHECK HERE IF HEADER IS A COOKIE
            if (header[0] == 'Cookie'):
                cookies = header[1].split(';')
                for c in cookies:
                    c = c.strip()
                    cookie_kv = c.split('=')
                    self.cookies[cookie_kv[0]] = cookie_kv[1].strip()
                    

def test1():
    request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\n')
    
    assert request.method == "GET"
    assert "Host" in request.headers 
    assert request.headers["Host"] == "localhost:8080"  # note: The leading space in the header value must be removed
    assert request.body == b""  # There is no body for this request.
    
    # When parsing POST requests, the body must be in bytes, not str

    # This is the start of a simple way (ie. no external libraries) to test your code.
    # It's recommended that you complete this test and add others, including at least one
    # test using a POST request. Also, ensure that the types of all values are correct

def test2():
    request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\nhello')
    
    assert request.method == "GET"
    assert request.path == "/"
    assert request.http_version == "HTTP/1.1"
    assert "Host" in request.headers 
    assert request.headers["Host"] == "localhost:8080"
    assert "Connection" in request.headers 
    assert request.headers["Connection"] == "keep-alive"
    assert request.body == b"hello" 

def test3():
    request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\nCookie: id=X6kAwpgW29M; visits=4\r\n\r\nhello')
    
    assert request.method == "GET"
    assert request.path == "/"
    assert request.http_version == "HTTP/1.1"
    assert "Host" in request.headers 
    assert request.headers["Host"] == "localhost:8080"
    assert "Connection" in request.headers 
    assert request.headers["Connection"] == "keep-alive"
    assert "id" in request.cookies
    assert request.cookies["id"] == "X6kAwpgW29M"
    assert "visits" in request.cookies 
    assert request.cookies["visits"] == "4"
    assert request.body == b"hello" 

def testprint():
    request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\nCookie: id=X6kAwpgW29M; visits=4\r\n\r\nhello')
    print(request.method)
    print(request.path)
    print(request.http_version)
    print(request.headers)
    print(request.cookies)
    print(request.body)

if __name__ == '__main__':
    test1()
    test2()
    test3()
    testprint()