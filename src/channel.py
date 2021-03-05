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
    # invalid channel
    if test_channel_is_invalid(channel_id):
        raise InputError()

    # invalid user
    if test_user_is_invalid(u_id):
        raise InputError() 

    # auth user (inviter) is not already a member of the channel
    if test_if_user_in_ch(auth_user_id, channel_id) == False:
        raise AccessError()
    
    # adding user to the channel 
    new_user_details = user_details(u_id)

    # insert relevant info into channel's info
    new_user = {}
    new_user['u_id'] = new_user_details['u_id']
    new_user['name_first'] = new_user_details['name_first']
    new_user['name_last'] = new_user_details['name_last']
    channels[channel_id]['all_members'].append(new_user)

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
    details['name'] = channels[channel_id]['name']
    details['owner_members'] = channels[channel_id]['owner_members']
    details['all_members'] = channels[channel_id]['all_members']
    
    return details
        

def channel_messages_v1(auth_user_id, channel_id, start):      
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_leave_v1(auth_user_id, channel_id):
    return {
    }

def channel_join_v1(auth_user_id, channel_id):
    return {
    }

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }