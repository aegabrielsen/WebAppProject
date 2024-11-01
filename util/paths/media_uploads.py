# import html
import uuid
import ffmpeg
from PIL import Image, ImageFile, ImageSequence
# from bson.objectid import ObjectId
from util.cookie_auth import *
from util.mongo import chat_collection
from util.multipart import parse_multipart
ImageFile.LOAD_TRUNCATED_IMAGES = True

def media_uploads(request, handler):
    print(request.body)
    multipart = parse_multipart(request)
    user_browser_id = request.cookies.get("user")
    user = cookie_auth(request)
    # invalid_user = False
    content = multipart.parts[0].content # Hardcoding it to assume the part at the 0th index is the image. Should be changed if feature is expanded
    print(content[0:50])
    if content.startswith(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01'):
        extension = "jpg"
    elif content.startswith(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00'):
        extension = "png"
    elif content.startswith(b'GIF89a'):
        extension = "gif"
        #b'GIF89a\xdc\x00\xdc\x00\xf7\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        #b'GIF89a\xe0\x01\xe0\x01\xf7\xff\x00Rs)\x00\x00\x00\xc5sB\x83:!\xff\xff\xff\x0b\x0b\x0b\x13\x13\x00\x1c\x1b\x00qn\x00\xff)\x19\xdeZ:\xff\xff\x00\xb5'
        #b'GIF89a\xdc\x00\xdc\x00\xf7\x00\x00\x0b\x0b\x0e\r\x11\x16\x13\x17\x1b\x15\x16\x17\x18\x12\x11\x18 (\x1b\r\x08\x1d"( )2!\x18\x15!&+"\x1d\x1c#'
        #b'GIF89a\xf4\x01w\x01\xf7\xfc\x00G/\x0231\x03;1\x03,2\x02 3\x02/3\x1603\x0b!4\x0b;6\x0bM6\x0fC7\x0f;9\x15\x0b'
    # elif content.startswith(b'\x00\x00\x00\x18ftypmp42\x00\x00\x00'):
    elif content.startswith(b'\x00\x00\x00'):
        extension = "mp4"
        #Content-Type: video/mp4\r\n\r\n\x00\x00\x00\x18ftypmp42\x00\x00\x00\x00isommp42\x00\x00\x15\x88moov\x00\x00\x00lmvhd\x00\x00\x00\x00\xdd\\.W\xdd\\.W\x00\x00\x03\xe8\x00\x00.X\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x
        #Content-Type: video/mp4\r\n\r\n\x00\x00\x00\x18ftypmp42\x00\x00\x00\x00isommp42\x00\x00\x13Lmoov\x00\x00\x00lmvhd\x00\x00\x00\x00\xdd\\1\x14\xdd\\1\x14\x00\x00\x03\xe8\x00\x00"\xb4\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\xf5meta\x00\x00\x00!hdlr\x00\x00\x00\x00\x00\x00\x00\x00mdta\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00dkeys\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x1bmdtacom.android.version\x00\x00\x00 mdtacom.android.manufacturer\x00\x00\x00\x19mdtacom.android.model\x00\x00\x00hilst\x00\x00\x00\x1a\x00\x00\x00\x01\x00\x00\x00\x12data\x00\x00\x00\x01\x00\x00\x00\x0010\x00\x00\x00 \x00\x00\x00\x02\x00\x00\x00\x18data\x00\x00\x00\x01\x00\x00\x00\x00motorola\x00\x00\x00&\x00\x00\x00\x03\x00\x00\x00\x1edata\x00\x00\x00\x01\x00\x00\x00\x0
        #                               \x00\x00\x00\x18ftypmp42\x00\x00\x00\x00mp41isom\x00\x00\x00(uuid\\\xa7\x08\xfb2\x8eB\x05\xa8ae\x0e\xca\n\x95\x96\x00\x00
        #                               \x00\x00\x00 ftypisom\x00\x00\x02\x00isomiso2avc1mp41\x00\x00\x00\x08free\x00\x146+mdat\x00\x00
    else:
        extension = "jpg"

    image_id = str(uuid.uuid4())
    filename = f"public/image/image{image_id}.{extension}"
    file = open(filename, "wb")
    file.write(content)
    file.close()
    if extension == 'mp4':
        try:
            probe = ffmpeg.probe(filename)
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            width = int(video_stream['width'])
            height = int(video_stream['height'])
            print(f'HEIGHT IS {height}')
            print(f'WIDTH IS {width}')
            if width > height:
                ffmpeg.input(filename).filter('scale', 238, -2).output(f"public/image/vid{image_id}.{extension}").run()
            else:
                ffmpeg.input(filename).filter('scale', -2, 238).output(f"public/image/vid{image_id}.{extension}").run()
        except ffmpeg.Error as e:
            print(f"Error: {e.stderr.decode('utf-8')}")
        # print('hello world')
    elif extension == 'gif':
        image = Image.open(filename)
        pics = []
        for pic in ImageSequence.Iterator(image):
            pic = pic.copy()
            pic.thumbnail((240, 240))
            pics.append(pic)
        pics[0].save(filename, save_all=True, append_images=pics[1:], optimize=False, duration=image.info['duration'], loop=0)
    else:
        image = Image.open(filename)
        image.thumbnail((240, 240))
        image.save(filename)
        print(image.size)
    
    #\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x13\x00\x00\x00\x11\x08\x06\x00\x00\x00?\x98\x97\xc7\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00
    #\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x13\x00\x00\x00\x11\x08\x06\x00\x00\x00?\x98\x97\xc7\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x
    #\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x06^\x00\x00\x02\xbf\x08\x02\x00\x00\x00\x87\x82\'t\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x12t\x00\x00\x12t\x01\xdef\x1fx\x00\x00N\xc9IDATx^\xed\xddYB\xe3\xc8\xb6\x05\xd0;.
    if user:
        if extension == 'mp4':
            chat_collection.insert_one({"username": user.get('username'), "message": f'<video controls><source src="public/image/vid{image_id}.{extension}" type="video/mp4"></video>', "user_browser_id": user_browser_id})
        else:
            chat_collection.insert_one({"username": user.get('username'), "message": f'<img src="public/image/image{image_id}.{extension}">', "user_browser_id": user_browser_id})
        #  width="240" height="240"
    else:
        if extension == 'mp4':
            chat_collection.insert_one({"username": "Guest", "message": f'<video controls><source src="public/image/vid{image_id}.{extension}" type="video/mp4"></video>', "user_browser_id": user_browser_id})
        else:
            chat_collection.insert_one({"username": "Guest", "message": f'<img src="public/image/image{image_id}.{extension}">', "user_browser_id": user_browser_id})
    response = f"HTTP/1.1 302 Found\r\nContent-Length: 0\r\nContent-Type: text/html; charset=utf-8\r\nLocation: /\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    handler.request.sendall(response.encode()) 