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
        