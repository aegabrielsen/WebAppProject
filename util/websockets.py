import hashlib
from base64 import b64encode
# from server import MyTCPHandler

def byte_to_binary_string(the_byte):
    as_binary = str(bin(the_byte))[2:]
    for _ in range(len(as_binary), 8):
        as_binary = '0' + as_binary
    return as_binary

def get_binary(bytes):
    return byte_to_binary_string((int.from_bytes(bytes, byteorder='big')))

def format_bytes(as_binary): # unused
    string = ''
    for i, b in enumerate(as_binary):
        string += b
        if (i + 1) % 8 == 0:
            string += ' '
        if (i + 1) % 32 == 0:
            string += '\n'
    return string

def binary_to_byte_chunks(binary):
    list = []
    temp = ''
    for i, b in enumerate(binary):
        temp += b
        if (i + 1) % 8 == 0:
            list.append(temp)
            temp = ''
    if len(temp) > 0:
        list.append(temp)
    return list

def byte_chunk_print(list):
    str = ''
    for i, s in enumerate(list):
        str += s
        str += ' '
        if (i + 1) % 4 == 0:
            str += '\n'
    return str
        
# ===== BYTE PRINTING STUFF ABOVE THIS LINE =====

def compute_accept(str):
    str += '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    str = hashlib.sha1(str.encode()).hexdigest()
    str = b64encode(bytes.fromhex(str)).decode()
    return str

def websocket_path(request, handler):
    print(request.headers)
    print(request.body)
    return

def parse_ws_frame(bstr: bytes):
    return Frame(bstr)


class Frame:
    def __init__(self, request: bytes):
        self.fin_bit = 0
        self.opcode = 0
        self.payload_length = 0
        self.payload = b''


def test1():
    key = 'PUWUNQyBpQBJU32c/TwqyQ=='
    accept = 'o4pUz3b+13iUPv87iPOQd1Nx2Sc='
    calc = compute_accept(key)
    assert calc == accept
    print("===== TEST1 PASSED =====")

def test2():
    frame_bytes = b'\x81\x9fgu\x8f\n\x1cW\xfbs\x17\x10\xad0E\x19\xe0m\x0e\x1b\xad&E\x1b\xeeg\x02W\xb5(-\x10\xfcy\x02W\xf2'
    # print(byte_to_binary_string(frame_bytes))
    # print(byte_to_binary_string((int.from_bytes(frame_bytes, byteorder='big'))))
    # print(format_bytes(byte_to_binary_string((int.from_bytes(frame_bytes, byteorder='big')))))
    # print(format_bytes(byte_to_binary_string((int.from_bytes(frame_bytes, byteorder='big')))))
    # print(binary_to_byte_chunks(byte_to_binary_string((int.from_bytes(frame_bytes, byteorder='big')))))
    # print(byte_chunk_print(binary_to_byte_chunks(byte_to_binary_string((int.from_bytes(frame_bytes, byteorder='big'))))))
    print(byte_chunk_print(binary_to_byte_chunks(get_binary(frame_bytes))))
    print(get_binary(frame_bytes))
    # print(binary_to_byte_chunks('1001101001'))
    expected_message = '{"type":"login","name":"Jesse"}'
    # frame = Frame(frame_bytes)
    # //frame.extractpayload()
    # assert len
    # assert decode
    print("===== TEST2 PASSED =====")

if __name__ == '__main__':
    test1()
    test2()