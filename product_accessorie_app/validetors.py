import re
def is_valid_username(username):
    pattern = r'^[a-zA-Z0-9_-]{3,15}$'
    match = re.match(pattern, username)
    return match is not None

def is_valid_bangladesh_phone_number(phone_number):
    pattern = r'^(\+?88)?01[3-9]\d{8}$'
    match = re.match(pattern, phone_number)
    return match is not None