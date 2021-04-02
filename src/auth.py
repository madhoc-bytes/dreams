'''auth functions implementation'''

from json import dumps
import re
import random
import hashlib
import smtplib
import ssl
import jwt
import data
from error import InputError, AccessError

def auth_login_v1(email, password):
    '''auth login function implementation'''
    if len(users) != 0:
        for user in users:
            if not email_is_valid(email):
                raise InputError
            if user['email'] == email and user['password'] == password:
                u_id = user['u_id']
            elif user['email'] != email:
                raise InputError
            elif user["password"] != password:
                raise InputError
    return u_id

def auth_register_v1(email, password, name_first, name_last):
    '''auth register function implementation'''
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
            elif handle_len <= 20:
                handle = name_first + name_last + unique_suffix
        n_users += 1
    if not email_is_valid(email):
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

def get_users():
    global users
    return users

def auth_register_v2(email, password, name_first, name_last):
    info = request.get_json()
    users_list = get_users()

    auth_user_id = len(users_list)
    
    new_token = generate_token(auth_user_id)

    #setting handle
    handle = (info[name_first] + info[name_last])
    handle = handle.lower()
    if len(users_list) != 0:
        for user in users_list:
            if user['email'] == info[email]:
                raise InputError


    n_users = 0

    for user in users_list:
        unique_suffix = str(n_users)
        handle_len = len(handle)
        if user['handle'] == handle:
            if handle_len > 20:
                handle = (info[name_first] + info[name_last])[:20] + unique_suffix
            elif handle_len <= 20:
                handle = info[name_first] + info[name_last] + unique_suffix
        n_users += 1
    if not email_is_valid(info[email]):
        raise InputError
    #checking len first and last name less than 50 and more than 1
    if len(info[name_first]) > 50 or  len(info[name_first]) <= 1 or len(info[name_last]) > 50 or len(info[name_last]) <= 1:
        raise InputError
    if not info[name_first].strip() or not info[name_last].strip():
        raise InputError

    #checking valid pass len
    if len(info[password]) < 6:
        raise InputError
    
    users_list.append({
            'email': info[email],
            'password': hash_password(info[password]),
            'name_first': info[name_first],
            'name_last': info[name_last],
            'handle': handle,
            'u_id': auth_user_id,
            'token': new_token,
            'permission_id': 0,
            'profile_img_url': None
        })
    if len(users_list) == 1:
            users_list[0]['permission_id'] = 1

    
    return dumps({
        'token': new_token,
        'auth_user_id': auth_user_id
    })

def auth_login_v2(email, password):
    info = request.get_json()
    users_list = get_users()

    if len(users_list) != 0:
        for user in users_lsit:
            if not email_is_valid(info[email]):
                raise InputError
            if user['email'] == info[email] and user['password'] == hash_password(info[password]):
                u_id = user['u_id']
                new_token = generate_token(u_id)
            elif user['email'] != info[email]:
                raise InputError
            elif user["password"] != infp[password]:
                raise InputError

    return dumps({
        'token': new_token,
        'auth_user_id': u_id
    })

def auth_logout_v2(token):
    is_success = False

    for user in users:
        if user['token'] == token:
            user['token'] = None
            is_success = True

    return dumps({'is_success': is_success})

def generate_token(u_id):
    token = jwt.encode({'u_id': u_id}, data.SECRET, algorithm='HS256').decode('UTF-8')
    return str(token)

def get_user_from_token(token):
    decoded_u_id = jwt.decode(token, data.SECRET, algorithms='HS256')
    return decoded_u_id['u_id']

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def email_is_valid(email):
    '''checking for a valid email using regex'''
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return bool(re.search(regex, email))

