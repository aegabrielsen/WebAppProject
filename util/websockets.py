import hashlib
from base64 import b64encode
from util.byte_formating import *
# from server import MyTCPHandler

def compute_accept(str):
    str += '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    str = hashlib.sha1(str.encode()).hexdigest()
    str = b64encode(bytes.fromhex(str)).decode()
    return str
    
def generate_ws_frame(bytes: bytes):
    ws_frame = b''
    byte_1 = 0b10000001 # fin bit of 1 and op code of 1
    ws_frame += byte_1.to_bytes(1, 'big')
    length = len(bytes)
    if length < 126:
        byte_2 = length
        ws_frame += byte_2.to_bytes(1, 'big')
    elif length >= 126 and length < 65536:
        byte_2 = 126
        ws_frame += byte_2.to_bytes(1, 'big')
        ws_frame += (length.to_bytes(2, byteorder = 'big'))
    elif length >= 65536:
        byte_2 = 127
        ws_frame += byte_2.to_bytes(1, 'big')
        ws_frame += (length.to_bytes(8, byteorder = 'big'))
    ws_frame += (bytes)
    return ws_frame



def parse_ws_frame(bytes: bytes):
    return Frame(bytes)

class Frame:
    def __init__(self, bytes: bytes):
        self.fin_bit = 0
        self.opcode = 0
        self.payload_length = 0
        self.payload = b''
        self.mask_bit = 0

        self.fin_bit = (bytes[0] & 0b10000000) >> 7
        self.opcode = (bytes[0] & 0b00001111)
        self.mask_bit = (bytes[1] & 0b10000000) >> 7
        self.payload_length = (bytes[1] & 0b01111111)

        cursor = 2
        temp_bytes = b''
        if self.payload_length == 126:
            temp_bytes += bytes[2].to_bytes(1, 'big')
            temp_bytes += bytes[3].to_bytes(1, 'big')
            self.payload_length = int.from_bytes(temp_bytes, 'big')
            cursor = 4
        elif self.payload_length == 127:
            for i in range(2, 10):
                temp_bytes += bytes[i].to_bytes(1, 'big')
            self.payload_length = int.from_bytes(temp_bytes, 'big')
            cursor = 10
        if self.mask_bit == 1:
            masks = []
            for i in range(4):
                masks.append(bytes[cursor])
                cursor += 1
            # print(masks)
        
        mask_idx = 0
        for i in range(cursor, len(bytes)):
            cur = bytes[i]
            if self.mask_bit == 1:
                cur = (cur ^ masks[mask_idx % 4])
                mask_idx += 1
            self.payload += cur.to_bytes(1, 'big')
      


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
    print(frame.payload.decode())
    # print(byte_to_binary_string(int.from_bytes(frame.payload, 'big')))
    # print(expected_message.encode())
    # print('----- FRAME.PAYLOAD UNMASKED BYTES -----')
    # print(byte_chunk_print(binary_to_byte_chunks(str(frame.payload))))
    # print(byte_chunk_print(binary_to_byte_chunks(byte_to_binary_string(int.from_bytes(frame.payload, 'big')))))
    print("===== TEST2 PASSED =====")

def test_len_126():
    frame_bytes = b'\x88\xFEgu\x8f\n\x1cW\xfbs\x17\x10\xad0E\x19\xe0m\x0e\x1b\xad&E\x1b\xeeg\x02W\xb5(-\x10\xfcy\x02W\xf2'

    frame = parse_ws_frame(frame_bytes)
    assert frame.fin_bit == 1
    assert frame.opcode == 8
    assert frame.payload_length == 26485
    print(frame.payload_length)
    print("===== test_len_126 PASSED =====")

def test_len_127():
    frame_bytes = b'\x81\xFFgu\x8f\n\x1cW\xfbs\x17\x10\xad0E\x19\xe0m\x0e\x1b\xad&E\x1b\xeeg\x02W\xb5(-\x10\xfcy\x02W\xf2'

    frame = parse_ws_frame(frame_bytes)
    assert frame.fin_bit == 1
    assert frame.opcode == 1
    assert frame.payload_length == 7455022031769697139
    print(frame.payload_length)
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

def test_create():
    gen = generate_ws_frame(b'\x04U\x8b\x02\x07\x10\x8d\x00E\x11\x80\x08\x06\x11\x8d\x02E\x11\x8e\x02\x02U\x85\x08%\x10\x8c\x08\x02U\x82')
    frame = parse_ws_frame(gen)
    assert frame.fin_bit == 1
    assert frame.opcode == 1
    assert frame.mask_bit == 0
    print(frame.payload_length)
    print('----- FRAME.PAYLOAD -----')
    print(frame.payload)

if __name__ == '__main__':
    # test1()
    test2()
    # test_len_126()
    # test_len_127()
    # test_convert()
    # test_no_mask()
    # test_create()