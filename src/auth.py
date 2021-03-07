#from src import data 
import re
from src.error import InputError
from src.data import users
from src.other import clear_v1

def email_is_valid(email):
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if (re.search(regex, email)):
        return True
    else:
        return False


def auth_login_v1(email, password):
    
    if len(users) != 0:
        for user in users:
            
            if email_is_valid(email) != True:
                raise InputError

            if (user['email'] == email and user['password'] == password):
                u_id = user['u_id']
            elif (user['email'] != email):
                print(email)
                print(user['email'])
                #print(u_id)
                print(user['u_id'])
                raise InputError
            elif (user["password"] != password):
                raise InputError

    return (u_id)


def auth_register_v1(email, password, name_first, name_last):
    #setting handle
    handle = (name_first + name_last)
    handle = handle.lower()
    
    if len(users) != 0:
        for user in users:
            if user['email'] == email:
                raise InputError


    n_users = 0

    for user in users:
        
        unique_suffix = str(n_users)
        handle_len = len(handle)

        if user['handle'] == handle:
            
            if handle_len > 20:
                handle = (name_first + name_last)[:20] + unique_suffix
                '''
                if handle == user['handle']:
                    handle = handle + unique_suffix
                '''   
            elif handle_len <= 20:
                handle = name_first + name_last + unique_suffix
                #print(n_users)
                '''
                if handle == user['handle']:
                    handle = handle + unique_suffix
                '''
        n_users += 1  

    if email_is_valid(email) != True:
            raise InputError
    #checking len first and last name less than 50 and more than 1 
    if len(name_first) > 50 or  len(name_first) <= 1 or len(name_last) > 50 or len(name_last) <= 1:
        raise InputError
    
    if not name_first.strip() or not name_last.strip():
        raise InputError

    #checking valid pass len
    if len(password) < 6:
            raise InputError


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
