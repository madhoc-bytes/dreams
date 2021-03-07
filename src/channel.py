from src.data import users, channels
from src.error import InputError, AccessError

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    # invalid channel
    if test_channel_is_invalid(channel_id):
        raise InputError()

    # invalid user  
    if test_if_user_in_ch(auth_user_id, channel_id) == False:
        raise AccessError()

    # insert info into dictionary
    details = {}
    details['name'] = channels[channel_id['id']]['name']
    details['owner_members'] = channels[channel_id['id']]['owner_members']
    details['all_members'] = channels[channel_id['id']]['all_members']
    
    return details


def channel_messages_v1(auth_user_id, channel_id, start): 
    '''Tests potential error cases'''
    if test_user_is_invalid(auth_user_id):
        raise InputError()
    if test_channel_is_invalid(channel_id):
        raise InputError()
    if test_if_user_in_ch(auth_user_id, channel_id) == False:
        raise AccessError()
    if start > len(channels[channel_id['id']]['messages']):
        raise InputError()
    '''Appends messages in channel to result, stops when has appended 50 or no more messages'''
    result = []
    i = 0
    for msg in channels[channel_id['id']]['messages']:
        result.append(msg)
        i += 1
        if i == 50:
            return {
                'messages': result,
                'start': start,
                'end': start + 50
            }

    return {
        'messages': result,
        'start': start,
        'end': -1,
    }

def channel_leave_v1(auth_user_id, channel_id):
    return {
    }

def channel_join_v1(auth_user_id, channel_id):
    '''Tests potential error cases'''
    if test_user_is_invalid(auth_user_id):
        raise InputError()
    if test_channel_is_invalid(channel_id):
        raise InputError()
    if channels[channel_id['id']]['is_public'] == False:
        raise AccessError()

    '''Gets relevant user information'''
    new_user_details = user_details(auth_user_id)
    new_user = {}
    new_user['name_first'] = new_user_details['name_first']
    new_user['name_last'] = new_user_details['name_last']
    new_user['u_id'] = new_user_details['u_id']

    '''Appends to 'all_members' key in dictionary'''
    channels[channel_id['id']]['all_members'].append(new_user)
    return {}

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

# CUSTOM FUNCTIONS

# Jeffery's functions
# ====================================================================
# tests if channel exists 
# returns False if it does
def test_channel_is_invalid(channel_id):
    if len(channels) == 0:
        return True
    for ch in channels:
        key, value = 'id', channel_id['id']
        if key in ch and value == ch[key]:
            return False
    return True    

# tests if user exists
# returns False if they do
def test_user_is_invalid(u_id):
    if len(users) == 0:
        return True

    for user in users:
        key, value = 'u_id', u_id['auth_user_id']
        if key in user and value == user[key]:
            return False
    return True  

# tests if user is in a channel
# returns True if they are
def test_if_user_in_ch(u_id, channel_id):
    if len(channels[channel_id['id']]['all_members']) == 0:
        return False

    for user in channels[channel_id['id']]['all_members']:
        key, value = 'u_id', u_id['auth_user_id']
        if key in user and value == user[key]:
            return True
    return False    

# give a u_id find a user's details and return them as a dict
def user_details(u_id):
    if len(users) == 0:
        return {}

    for user in users:
        key, value = 'u_id', u_id['auth_user_id']
        if key in user and value == user[key]:
            return user            
# ====================================================================
