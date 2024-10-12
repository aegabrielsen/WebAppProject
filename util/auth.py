def extract_credentials(request):
    line = request.body.decode().split('&')
    username = line[0].split('=', 1)[1]
    password = line[1].split('=', 1)[1]
    percents = ['%21', '%40', '%23', '%24', '%25', '%5E', '%26', '%28', '%29', '%2D', '%5F', '%3D']
    numbers = ['!', '@', '#', '$', '%', '^', '&', '(', ')', '-', '_', '=']
    for i, p in enumerate(percents):
        password = password.replace(p, numbers[i])
    return [username, password] # Username and password both as strings

def validate_password(password):
    if len(password) < 8:
        return False
    special_char = ['!', '@', '#', '$', '%', '^', '&', '(', ')', '-', '_', '=']
    lower, upper, number, special = False, False, False, False,

    for c in password:
        if (ord(c) >= ord('A') and ord(c) <= ord('Z')):
            upper = True
            continue
        if (ord(c) >= ord('a') and ord(c) <= ord('z')):
            lower = True
            continue
        if (ord(c) >= ord('0') and ord(c) <= ord('9')):
            number = True
            continue
        if c in special_char:
            special = True
            continue
        return False # if the for loop reaches this then it is not a valid character

    return lower and upper and number and special

def test1():
    assert validate_password('test') == False
    assert validate_password('Aa1!1234') == True
    assert validate_password('Aaa!aaaa') == False
    assert validate_password('AA1!1234') == False
    assert validate_password('aa1!1234') == False
    assert validate_password('Aa1a1234') == False
    assert validate_password('Aa1a123') == False
    assert validate_password('Aa1!1234aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa') == True
    assert validate_password('Aa1a1234,') == False
    assert validate_password('Aa1a1234^') == True
    assert validate_password('Aa1a1!@#$%^&()-_=') == True

if __name__ == '__main__':
    test1()

