from src.error import InputError, AccessError
from src.channel import token_to_id
from src.data import users, dms, channels
from datetime import datetime, timezone

def message_senddm_v2(token, dm_id, message):
    #import uid from token
    token_uid = token_to_id(token)
    if not test_if_user_in_dm(token_uid, dm_id):
        raise AccessError('authorised user has not joined the channel they are trying to post to')
    #InputError when any of:
    #Message is more than 1000 characters
    if len(message) > 1000:
        raise InputError('Message is more than 1000 characters')
    return {
        'message_id': messagesendreturn(dm_id, token_uid, message),
    }

def test_if_user_in_dm(u_id, dm_id):
    # if all_members is empty in given dm, then obviously invalid
    if len(dms[dm_id]['all_members']) == 0:
        return False

    for user in dms[dm_id]['all_members']:
        key, value = 'u_id', u_id
        if key in user and value == user[key]:
            return True
    return False

def is_member_exist(u_id, dm_id): 
    for dm in dms: 
        if dm['dm_id'] == dm_id: 
            for member in dm['members']: 
                if u_id == member['u_id']: 
                    return True 
    return False

def messagesendreturn(dm_id, u_id, message): 
    total_messages = num_message() 
    for dm in dms: 
        if dm['dm_id'] == dm_id:
            break

    m_time = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    message_send = { 
        'message_id': total_messages + 1, 
        'u_id': u_id, 
        'message': message,
        'time_created': m_time,
        'reacts': [],
        'is_pinned': False,
    } 
    dm['messages'].append(message_send)
    return message_send['message_id']

def num_message():
    total = -1
    for channel in channels:
        for message in channel['messages']:
            total = total + len(message)
    
    for dm in dms:
        for message in dm['messages']:
            total = total + len(message)
    
    return total 