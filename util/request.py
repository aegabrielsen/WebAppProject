class Request:

    def __init__(self, request: bytes):
        # TODO: parse the bytes of the request and populate the following instance variables
        
        self.body = b""
        self.method = ""
        self.path = ""
        self.http_version = ""
        self.headers = {} # Note: The raw Cookies header should still be in your headers dictionary even after parsing the individual cookies in the cookies dictionary. -a
        self.cookies = {} # Be sure to trim white space -a
        
        # print(request)
        # print(request.decode())
        lines = request.split(b'\r\n')
        # print(lines)
        status_line = lines.pop(0).split(b' ') # No error checking. Consider checking if length != 3
        self.method = status_line[0].decode()
        self.path = status_line[1].decode()
        self.http_version = status_line[2].decode()

        # print(lines)
        body_line = False
        for l in lines:
            if body_line: # Should be last line
                self.body = l
                break
            if l == b'': # First \r\n that signifies the next line is the body
                body_line = True
                continue
            # At this point l should be a header
            header = l.decode().split(':', 1)
            # new_header = {header[0]: header[1].strip()}
            self.headers[header[0]] = header[1].strip()
            # TODO: CHECK HERE IF HEADER IS A COOKIE





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
    assert "Host" in request.headers 
    assert request.headers["Connection"] == "keep-alive"
    assert request.body == b"hello" 

if __name__ == '__main__':
    test1()
    test2()
