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
    accept = compute_accept(request.headers.get('Sec-WebSocket-Key', 0))
    response = f"HTTP/1.1 101 Switching Protocols\r\nContent-Length: 0\r\nConnection: Upgrade\r\nUpgrade: websocket\r\nSec-WebSocket-Accept: {accept}\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    handler.request.sendall(response.encode()) 

def parse_ws_frame(bstr: bytes):
    return Frame(bstr)


class Frame:
    def __init__(self, bytes: bytes):
        self.fin_bit = 0
        self.opcode = 0
        self.payload_length = 0
        self.payload = b''
        byte_chunks = binary_to_byte_chunks(get_binary(bytes))
        self.fin_bit = int(byte_chunks[0][0])
        self.opcode = int(byte_chunks[0][4] + byte_chunks[0][5] + byte_chunks[0][6] + byte_chunks[0][7], 2)
        print(f"Opcode is {self.opcode}")
        mask_bit = int(byte_chunks[1][0])
        temp = ''
        for x in range(1, 8):
            temp += byte_chunks[1][x]
        self.payload_length = int(temp, 2)
        print(f"payload_length is {self.payload_length}")
        cursor = 2
        if(self.payload_length == 126):
            temp_bytes = byte_chunks[2] + byte_chunks[3]
            temp = ''
            for x in range(0, 16):
                temp += temp_bytes[x]
            # print(temp)
            self.payload_length = int(temp, 2)
            cursor = 4
        elif(self.payload_length == 127):
            temp_bytes = ''
            for x in range(2, 10):
                temp_bytes += byte_chunks[x]
            temp = ''
            for x in range(0, 64):
                temp += temp_bytes[x]
            # print(temp)
            self.payload_length = int(temp, 2)
            cursor = 10

        # if(mask_bit == 1):
        #     full_mask = ''
        #     full_mask += byte_chunks[cursor]
        #     cursor += 1
        #     full_mask += byte_chunks[cursor]
        #     cursor += 1
        #     full_mask += byte_chunks[cursor]
        #     cursor += 1
        #     full_mask += byte_chunks[cursor]
        #     cursor += 1
        #     print(full_mask)
        # mask_idx = 0
        # # print(len(byte_chunks))
        # print(self.payload_length)
        # for x in range(cursor, len(byte_chunks), 4):
        #     cur = byte_chunks[x]
        #     if(x + 1 < len(byte_chunks)):
        #         cur += byte_chunks[x + 1]
        #     if(x + 2 < len(byte_chunks)):
        #         cur += byte_chunks[x + 2]
        #     if(x + 3 < len(byte_chunks)):
        #         cur += byte_chunks[x + 3]
        #     if(mask_bit == 1):
        #         print(cur)
        #         # print(bin(masking_keys[mask_idx % 4]).replace("0b", ""))
        #         cur = int(cur)
        #         cur = str(bin(cur ^ int(full_mask)).replace("0b", ""))
        #         print(cur)
        #         print('===')
        #         mask_idx + 1
        #     self.payload += cur.encode()


        if(mask_bit == 1):
            masking_keys = []
            masking_keys.append(int(byte_chunks[cursor], 2))
            cursor += 1
            masking_keys.append(int(byte_chunks[cursor], 2))
            cursor += 1
            masking_keys.append(int(byte_chunks[cursor], 2))
            cursor += 1
            masking_keys.append(int(byte_chunks[cursor], 2))
            cursor += 1
            # print(masking_keys)
        mask_idx = 0
        # print(len(byte_chunks))
        # print(self.payload_length)
        for x in range(cursor, len(byte_chunks)):
            cur = byte_chunks[x]
            if(mask_bit == 1):
                # print('cur')
                # print(cur)
                # print(bin(masking_keys[mask_idx % 4]).replace("0b", ""))
                
                # print('cur, 2')
                cur = int(cur, 2)
                # print(cur)
                # print('masking key')
                # print(masking_keys[mask_idx % 4])
                cur = str(bin(cur ^ masking_keys[mask_idx % 4]).replace("0b", ""))
                
                # print('cur after')
                # print(cur)
                # print('===')
                mask_idx += 1
            self.payload += cur.encode()

        




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
    
    print('----- FULL BYTES FROM FRAME -----')
    print(byte_chunk_print(binary_to_byte_chunks(get_binary(frame_bytes))))
    print('----- FULL BINARY FROM FRAME -----')
    print(get_binary(frame_bytes))
    # print(int('00000011', 2))

    # print(binary_to_byte_chunks('1001101001'))
    expected_message = '{"type":"login","name":"Jesse"}'
    frame = parse_ws_frame(frame_bytes)
    assert frame.fin_bit == 1
    assert frame.opcode == 1
    print('----- FRAME.PAYLOAD LENGTH -----')
    print(frame.payload_length)
    # //frame.extractpayload()
    # assert len
    # assert decode
    print('----- len(frame.payload) LENGTH -----')
    print(len(frame.payload))
    print('----- FRAME.PAYLOAD -----')
    print(frame.payload)
    print('----- FRAME.PAYLOAD UNMASKED BYTES -----')
    print(byte_chunk_print(binary_to_byte_chunks(str(frame.payload))))
    print("===== TEST2 PASSED =====")

def test_len_126():
    frame_bytes = b'\x88\xFEgu\x8f\n\x1cW\xfbs\x17\x10\xad0E\x19\xe0m\x0e\x1b\xad&E\x1b\xeeg\x02W\xb5(-\x10\xfcy\x02W\xf2'

    frame = parse_ws_frame(frame_bytes)
    assert frame.fin_bit == 1
    assert frame.opcode == 8
    assert frame.payload_length == 26485
    print("===== test_len_126 PASSED =====")

def test_len_127():
    frame_bytes = b'\x81\xFFgu\x8f\n\x1cW\xfbs\x17\x10\xad0E\x19\xe0m\x0e\x1b\xad&E\x1b\xeeg\x02W\xb5(-\x10\xfcy\x02W\xf2'

    frame = parse_ws_frame(frame_bytes)
    assert frame.fin_bit == 1
    assert frame.opcode == 1
    assert frame.payload_length == 7455022031769697139
    print("===== test_len_127 PASSED =====")

def test_convert():
    frame_bytes = b'\x81\x9fgu\x8f\n\x1cW\xfbs\x17\x10\xad0E\x19\xe0m\x0e\x1b\xad&E\x1b\xeeg\x02W\xb5(-\x10\xfcy\x02W\xf2'
    expected_message = '{"type":"login","name":"Jesse"}'
    frame = parse_ws_frame(frame_bytes)
    assert frame.fin_bit == 1
    assert frame.opcode == 1

    # print(len(frame.payload))
    # binary_int = int(frame.payload.decode(), 2)
    binary_int = int((frame.payload), 2)
    # binary_int = int("11000010110001001100011", 2)
    print(binary_int)
    byte_number = binary_int.bit_length() + 7 // 8
    print(byte_number)
    binary_array = binary_int.to_bytes(byte_number, "big")
    print(binary_array)
    ascii_text = binary_array.decode('latin-1')
    print(ascii_text)
    print(byte_chunk_print(binary_to_byte_chunks(str(frame.payload))))
    print("===== test_convert PASSED =====")

def test_no_mask():
    frame_bytes = b'\x81\x1fgu\x8f\n\x1cW\xfbs\x17\x10\xad0E\x19\xe0m\x0e\x1b\xad&E\x1b\xeeg\x02W\xb5(-\x10\xfcy\x02W\xf2'
    # print(byte_to_binary_string(frame_bytes))
    # print(byte_to_binary_string((int.from_bytes(frame_bytes, byteorder='big'))))
    # print(format_bytes(byte_to_binary_string((int.from_bytes(frame_bytes, byteorder='big')))))
    # print(format_bytes(byte_to_binary_string((int.from_bytes(frame_bytes, byteorder='big')))))
    # print(binary_to_byte_chunks(byte_to_binary_string((int.from_bytes(frame_bytes, byteorder='big')))))
    # print(byte_chunk_print(binary_to_byte_chunks(byte_to_binary_string((int.from_bytes(frame_bytes, byteorder='big'))))))
    
    print('----- FULL BYTES FROM FRAME -----')
    print(byte_chunk_print(binary_to_byte_chunks(get_binary(frame_bytes))))
    print('----- FULL BINARY FROM FRAME -----')
    print(get_binary(frame_bytes))
    # print(int('00000011', 2))

    # print(binary_to_byte_chunks('1001101001'))
    expected_message = '{"type":"login","name":"Jesse"}'
    frame = parse_ws_frame(frame_bytes)
    assert frame.fin_bit == 1
    assert frame.opcode == 1
    print('----- FRAME.PAYLOAD LENGTH -----')
    print(frame.payload_length)
    # //frame.extractpayload()
    # assert len
    # assert decode
    print('----- len(frame.payload) LENGTH -----')
    print(len(frame.payload))
    print('----- FRAME.PAYLOAD -----')
    print(frame.payload)
    print('----- FRAME.PAYLOAD UNMASKED BYTES -----')
    print(byte_chunk_print(binary_to_byte_chunks(str(frame.payload))))
    print("===== test_no_mask PASSED =====")

if __name__ == '__main__':
    test1()
    test2()
    test_len_126()
    test_len_127()
    # test_convert()
    # test_no_mask()