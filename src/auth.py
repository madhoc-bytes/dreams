#from src import data 
import re
from src.error import InputError
from src.data import users


def auth_login_v1(email, password):
    return {
        'auth_user_id': 1,
    }

def auth_register_v1(email, password, name_first, name_last):

    #check for valid email
    if email_is_valid(email):
        for user in users:
            if user['email'] == email:
                raise InputError

    
    #checking len first and last name less than 50 and more than 1 
    if len(name_first) > 50 or not name_first or len(name_last) > 50 or not name_last:
        raise InputError(description='First or Last Name not between 1 and 50 characters')
    
    if not name_first.strip() or not name_last.strip():
        raise InputError(description='First or Last Name can not be all spaces')

    #checking valid pass len
    if len(password) < 6:
            raise InputError(description='Password less then 6 characters long')

    #setting handle
    handle = (name_first + name_last)
    handle = handle.lower()

    auth_user_id = len(users)

    
    for user in users:
        n = 0
        handle_len = len(handle)
        if user['handle'] == handle[:len(handle)]:
            #handle_len = len(handle)
            if handle_len > 20:
                handle = handle[:20] + n
            else:
                handle = handle + n
            n += 1

    #adding info to data structure
    users.append({
            'email': email,
            'password': password,
            'name_first': name_first,
            'name_last': name_last,
            'handle': handle,
            'auth_user_id': auth_user_id,
        })

    return {
        'auth_user_id': auth_user_id,
    }

def email_is_valid(email):
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return (re.search(regex, email))
