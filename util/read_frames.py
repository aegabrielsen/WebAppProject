from util.byte_formating import *

class Two_Bytes:
    def __init__(self, bytes: bytes):
        self.fin_bit = 0
        self.opcode = 0
        self.payload_length = 0
        self.mask_bit = 0
        byte_chunks = binary_to_byte_chunks(get_binary(bytes))
        self.fin_bit = int(byte_chunks[0][0])
        self.opcode = int(byte_chunks[0][4] + byte_chunks[0][5] + byte_chunks[0][6] + byte_chunks[0][7], 2)

        self.mask_bit = int(byte_chunks[1][0])
        temp = ''
        for x in range(1, 8):
            temp += byte_chunks[1][x]
        self.payload_length = int(temp, 2)
        print(f"Opcode is {self.opcode}")
        print(f"Fin bit is {self.fin_bit}")
        print(f"Mask bit is {self.mask_bit}")
        print(f"Payload length is {self.payload_length}")


def while_reading_frames(handler):
    while True:
        received_data = handler.request.recv(2)
        bytes_to_read = 0
        two_bytes = Two_Bytes(received_data)
        if two_bytes.opcode == 8:
            break
        if two_bytes.mask_bit == 1:
            bytes_to_read += 4
        if two_bytes.payload_length < 126:
            payload_length = two_bytes.payload_length
        elif two_bytes.payload_length == 126:
            # get two more bytes
            temp = handler.request.recv(2) # temp will be the real payload length
            received_data += temp # Add the two extra bytes to received_data
            payload_length = int(get_binary(temp), 2)
        elif two_bytes.payload_length == 127:
            # get way more
            temp = handler.request.recv(8) # temp will be the real payload length
            received_data += temp # Add the two extra bytes to received_data
            payload_length = int(get_binary(temp), 2)
        bytes_to_read += payload_length
        received_data += handler.request.recv(bytes_to_read)

        print(received_data)