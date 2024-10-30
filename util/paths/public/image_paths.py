def cat_path(request, handler):
    f = open("public/image/cat.jpg", "rb")
    file_contents = f.read()
    response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(file_contents)}\r\nContent-Type: image/jpeg; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    response = response.encode() + file_contents
    handler.request.sendall(response)

def dog_path(request, handler):
    f = open("public/image/dog.jpg", "rb")
    file_contents = f.read()
    response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(file_contents)}\r\nContent-Type: image/jpeg; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    response = response.encode() + file_contents
    handler.request.sendall(response)

def eagle_path(request, handler):
    f = open("public/image/eagle.jpg", "rb")
    file_contents = f.read()
    response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(file_contents)}\r\nContent-Type: image/jpeg; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    response = response.encode() + file_contents
    handler.request.sendall(response)

def elephant_small_path(request, handler):
    f = open("public/image/elephant-small.jpg", "rb")
    file_contents = f.read()
    response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(file_contents)}\r\nContent-Type: image/jpeg; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    response = response.encode() + file_contents
    handler.request.sendall(response)

def elephant_path(request, handler):
    f = open("public/image/elephant.jpg", "rb")
    file_contents = f.read()
    response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(file_contents)}\r\nContent-Type: image/jpeg; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    response = response.encode() + file_contents
    handler.request.sendall(response)

def flamingo_path(request, handler):
    f = open("public/image/flamingo.jpg", "rb")
    file_contents = f.read()
    response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(file_contents)}\r\nContent-Type: image/jpeg; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    response = response.encode() + file_contents
    handler.request.sendall(response)

def kitten_path(request, handler):
    f = open("public/image/kitten.jpg", "rb")
    file_contents = f.read()
    response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(file_contents)}\r\nContent-Type: image/jpeg; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    response = response.encode() + file_contents
    handler.request.sendall(response)

def uploaded_image(request, handler):
    image_path = request.path
    image_path = image_path.split("/image/", 1)[1]
    image_path = image_path.replace("/", "")
    # print(image_path)
    f = open(f"public/image/{image_path}", "rb")
    file_contents = f.read()
    extension = image_path.split(".")[1]
    if extension == "mp4":
        response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(file_contents)}\r\nContent-Type: video/mp4; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    elif extension == "jpg":
        response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(file_contents)}\r\nContent-Type: image/jpeg; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    else:
        response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(file_contents)}\r\nContent-Type: image/{extension}; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    response = response.encode() + file_contents
    handler.request.sendall(response)