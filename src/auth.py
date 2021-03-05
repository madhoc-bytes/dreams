import re
from src.error import InputError
from src.data import users

def email_is_valid(email):
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return (re.search(regex, email))

def auth_register_v1(email, password, name_first, name_last):
    #setting handle
    handle = (name_first + name_last)
    handle = handle.lower()
    
    if len(users) != 0:
        #check for valid email
        if email_is_valid(email) != True:
            raise InputError
        for user in users:
            if user['email'] == email:
                raise InputError

        for user in users:
            n_users = 0
        
        unique_suffix = str(n_users)
        handle_len = len(handle)
        if user['handle'] == handle[:len(handle)]:
            #handle_len = len(handle)
            if handle_len > 20:
                handle = handle[:20] + unique_suffix
            else:
                handle = handle + unique_suffix
            n_users += 1
    
    #checking len first and last name less than 50 and more than 1 
    if len(name_first) > 50 or not name_first or len(name_last) > 50 or not name_last:
        raise InputError(description='First or Last Name not between 1 and 50 characters')
    
    if not name_first.strip() or not name_last.strip():
        raise InputError(description='First or Last Name can not be all spaces')

    #checking valid pass len
    if len(password) < 6:
            raise InputError(description='Password less then 6 characters long')



    auth_user_id = len(users)

    #adding info to data structure
    users.append({
            'email': email,
            'password': password,
            'name_first': name_first,
            'name_last': name_last,
            'handle': handle,
            'u_id': auth_user_id,
        })

    return {'auth_user_id': auth_user_id}


