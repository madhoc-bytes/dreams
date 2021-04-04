'''auth functions implementation'''

from json import dumps
import re
import random
import hashlib
import smtplib
import ssl
import jwt
from src.data import users
from src import data

from src.error import InputError, AccessError

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
    if not is_email_used:
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

    new_token = generate_token(auth_user_id)

    permission_id = False

    #adding info to data structure
    users.append({
            'email': email,
            'password': password,
            'name_first': name_first,
            'name_last': name_last,
            'handle': handle,
            'u_id': auth_user_id,
            'token': new_token,
            'permission_id': permission_id
        })

    if len(users) == 1:
            users[0]['permission_id'] = 1

    
    return {
        'token': new_token,
        'auth_user_id': auth_user_id
    }

def auth_login_v2(email, password):
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
    SECRET = 'break'
    token = jwt.encode({'u_id': u_id}, SECRET, algorithm='HS256')
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

def is_email_used(email):
    used = False
    for user in users:
        if user['email'] == email:
            used = True
    return used


#request.form.get only for POST and PUT
#