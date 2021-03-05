from src.data import users, channels
from src.error import InputError, AccessError

# tests if channel exists
# returns False if it does
def test_channel_is_invalid(channel_id):
    for ch in channels:
        key, value = 'id', channel_id
        if key in ch and value == ch[key]:
            return False
    return True    

# tests if user exists
# returns False if they do
def test_user_is_invalid(u_id):
    for user in users:
        key, value = 'id', u_id
        if key in user and value == user[key]:
            return False
    return True  

# tests if user is in a channel
# returns True if they are
def test_if_user_in_ch(u_id, channel_id):
    for user in channels[channel_id]['all_members']:
        key, value = 'u_id', u_id
        if key in user and value == user[key]:
            return True
    return False    

# give a u_id find a user's details and return them as a dict
def user_details(u_id):
    for user in users:
        key, value = 'u_id', u_id
        if key in user and value == user[key]:
            return user

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

def channel_messages_v1(auth_user_id, channel_id, start): 
    if test_channel_is_invalid(channel_id):
        raise InputError()
    if test_if_user_in_ch(auth_user_id, channel_id) == False:
        raise AccessError()
    if start > len(channels[channel_id]['messages']):
        raise InputError()
    result = []
    i = 0
    for msg in channels[channel_id]['messages']:
        result.append(msg)
        i += 1
        if i == 50:
            return {
                'messages': result
                'start': start,
                'end': start + 50
            }

    return {
        'messages': result
        'start': start,
        'end': -1,
    }

def channel_leave_v1(auth_user_id, channel_id):
    return {
    }

def channel_join_v1(auth_user_id, channel_id):
    if test_channel_is_invalid(channel_id):
        raise InputError()
    if channels[channel_id]['public'] == False:
        raise AccessError()

    new_user_details = user_details(auth_user_id)

    new_user = {}
    new_user['u_id'] = new_user_details['u_id']
    new_user['name_first'] = new_user_details['name_first']
    new_user['name_last'] = new_user_details['name_last']

    channels[channel_id]['all_members'].append(new_user)
    return {}

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }