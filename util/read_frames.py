from util.byte_formating import *
from util.websockets import *
from util.mongo import *
from util.cookie_auth import *
import json
import html
import uuid
import pymongo
from bson import json_util 
handler_set = {}

class Two_Bytes:
    def __init__(self, bytes: bytes):
        self.fin_bit = 0
        self.opcode = 0
        self.payload_length = 0
        self.mask_bit = 0
        binary = get_binary(bytes)
        print(binary)
        length_zeroes = 16 - len(binary)
        leading_zeroes = ''
        for i in range(length_zeroes):
            leading_zeroes += '0'
        binary = leading_zeroes + binary
        print(f'binary after leading zeroes {binary}')
        byte_chunks = binary_to_byte_chunks(binary)
        self.fin_bit = int(byte_chunks[0][0])
        self.opcode = int(byte_chunks[0][4] + byte_chunks[0][5] + byte_chunks[0][6] + byte_chunks[0][7], 2)

        self.mask_bit = int(byte_chunks[1][0])
        # print(byte_chunks[0])
        print(f"Opcode is {self.opcode}")
        print(f"Fin bit is {self.fin_bit}")
        print(f"Mask bit is {self.mask_bit}")
        # print(f"Payload length is {self.payload_length}")

        temp = ''
        for x in range(1, 8):
            # print(byte_chunks[1])
            temp += byte_chunks[1][x]
        self.payload_length = int(temp, 2)
        print(f"Opcode is {self.opcode}")
        print(f"Fin bit is {self.fin_bit}")
        print(f"Mask bit is {self.mask_bit}")
        print(f"Payload length is {self.payload_length}")


def while_reading_frames(request, handler):
    payload_buffer = b''
    session_id = uuid.uuid4()
    handler_set[session_id] = handler
    user = cookie_auth(request)
    username = 'Guest'
    if user:
        username = user.get('username')
    while True:
        received_data = handler.request.recv(2)
        bytes_to_read = 0
        two_bytes = Two_Bytes(received_data)
        if two_bytes.opcode == 8:
            del handler_set[session_id]
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
        # length_received = 0
        while bytes_to_read > 0:
        # received_temp = handler.request.recv(bytes_to_read)
            if bytes_to_read > 2048:
                received_temp = handler.request.recv(2048)
            else:
                received_temp = handler.request.recv(bytes_to_read)
            received_data += received_temp
            bytes_to_read -= len(received_temp)
        # length_received += len(received_temp)


        # print(received_data)
        print('--- Frame ---')
        frame = Frame(received_data)

        if frame.fin_bit == 0:
            payload_buffer += frame.payload
        else: # fin_bit == 1
            print(frame.fin_bit)
            print(frame.mask_bit)
            print(frame.opcode)
            print(frame.payload_length)
            print(f'the len(frame.payload) is {len(frame.payload)}')
            print(f'the frame.payload is {frame.payload}')
            # print(frame.payload)
            if len(payload_buffer) > 0:
                full_payload = payload_buffer
                full_payload += frame.payload
                print(f'payload_buffer: {len(payload_buffer)}, frame.payload: {len(frame.payload)}')
                payload_buffer = b''
            else:
                full_payload = frame.payload
            # full_payload = frame.payload
            # full_payload += payload_buffer
            print(f'the full payload is: {full_payload}')
            json_data = json.loads(full_payload.decode())
            if 'messageType' in json_data:
                if json_data["messageType"] == "chatMessage":
                    if 'message' in json_data:
                        # result = chat_post(request, json_data["message"])
                        result = chat_collection.insert_one({"username": username, "message": html.escape(json_data["message"])}).inserted_id
                        # print(result)
                        chat = chat_collection.find_one({"_id" : result})
                        # print(chat['message'])
                        new_message = { 'messageType': 'chatMessage', 'username': chat['username'], 'message': chat['message'], 'id': chat['_id']}
                        # new_message = json.dumps(new_message).encode()
                        new_message = json_util.dumps(new_message).encode()
                        # print(new_message)
                        
                        for i in handler_set:
                            # print(i)
                            handler_set[i].request.sendall(generate_ws_frame(new_message)) #list or dict of handlers and then send to all of them
                        # { username: "Guest", message: "test", user_browser_id: "10b480c0-cef6-4e67-a2ae-561ab9c03438", … }
                if json_data["messageType"] == "webRTC-offer" or json_data["messageType"] == "webRTC-answer" or json_data["messageType"] == "webRTC-candidate":
                    for i in handler_set:
                        if i != session_id:
                            handler_set[i].request.sendall(generate_ws_frame(full_payload))
                            break


'''
def chat_post(request, message):
    # message_obj = json.loads(request.body)
    # sent_xsrf_token = message_obj["xsrf_token"]
    user_browser_id = request.cookies.get("user")
    user = cookie_auth(request)
    # invalid_user = False
    if user:
        # if user.get('xsrf_token') == sent_xsrf_token:
        result = chat_collection.insert_one({"username": user.get('username'), "message": html.escape(message), "user_browser_id": user_browser_id})
                      # else:
        #     invalid_user = True
    else:
        result = chat_collection.insert_one({"username": "Guest", "message": html.escape(message), "user_browser_id": user_browser_id})
    return result.inserted_id
'''