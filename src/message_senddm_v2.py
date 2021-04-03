from src.error import InputError, AccessError
import jwt
from src.data import users, dms

def message_senddm_v2(token, dm_id, message):
    #check valid token#
    check_if_token_valid(token)
    #import uid from token
    token_uid = importuIDfromtoken(token)
    if not test_if_user_in_dm(token_uid, dm_id):
        raise AccessError('authorised user has not joined the channel they are trying to post to')
    #InputError when any of:
    #Message is more than 1000 characters
    if len(message) > 1000:
        raise InputError('Message is more than 1000 characters')
    return {
        'message_id': messagesendreturn(dm_id, token_uid, message),
    }

def check_if_token_valid(token):
    if not if_token_exit(token) or token == None:
        raise AccessError('Invalid Token')
    return

def if_token_exit(token):
    for user in users:
        if token == user[token]:
            return user
    return False

def importuIDfromtoken(token):
     '''Input a token, return its corresponding u_id''' 
    u_id_jwt = jwt.decode(token.encode(), SECRET, algorithms=['HS256']) 
    u_id = int(u_id_jwt['u_id'])
    return u_id

def is_member_exist(u_id, dm_id): 
    for dm in dms: 
        if dm['dm_id'] == dm_id: 
            for member in dm['members']: 
                if u_id == member['u_id']: 
                    return True 
    return False

def messagesendreturn(dm_id, u_id, message): 
    for dm in dms: 
        if dm['dm_id'] == dm_id:
            message_send = { 'message_id': num_message, 
                            'u_id': u_id, 
                            'message': message,  
                            } 
            dm['messages'].append(message_send) 
            num_message += 1 
        return message_send['message_id']