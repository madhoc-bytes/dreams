from src.data import users, channels
from src.error import InputError, AccessError

def channel_invite_v2(token, channel_id, u_id):
    auth_user_id = token_to_id(token)

    # invalid channel
    if test_channel_is_invalid(channel_id):
        raise InputError()

    # invalid user
    if test_user_is_invalid(u_id):
        raise InputError()

    # auth user (inviter) is not already a member of the channel
    if not test_if_user_in_ch(auth_user_id, channel_id):
        raise AccessError()

    # acquiring the details of the user (invitee)
    new_member_details = user_details(u_id)

    # insert user's relevant info (first name, last name and id) into channel's info
    new_member = {}
    new_member['name_first'] = new_member_details['name_first']
    new_member['name_last'] = new_member_details['name_last']
    new_member['u_id'] = new_member_details['u_id']
    channels[channel_id]['all_members'].append(new_member)

    return {}


def channel_details_v2(token, channel_id):
    auth_user_id = token_to_id(token)
    # invalid channel
    if test_channel_is_invalid(channel_id):
        raise InputError()
    
    # invalid user
    if not test_if_user_in_ch(auth_user_id, channel_id):
        raise AccessError()

    # insert info into dictionary and return it
    details = {}
    details['name'] = channels[channel_id]['name']
    details['is_public'] = channels[channel_id]['is_public']
    details['owner_members'] = channels[channel_id]['owner_members']
    details['all_members'] = channels[channel_id]['all_members']
    return details


def channel_messages_v1(auth_user_id, channel_id, start): 
    '''Tests potential error cases'''
    if test_user_is_invalid(auth_user_id):
        raise InputError()
    if test_channel_is_invalid(channel_id):
        raise InputError()
    if not test_if_user_in_ch(auth_user_id, channel_id):
        raise AccessError()
    if start > len(channels[channel_id]['messages']):
        raise InputError()
    '''Appends messages in channel to result, stops when has appended 50 or no more messages'''
    result = []
    i = 0
    for msg in channels[channel_id]['messages']:
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

'''
def channel_leave_v1(auth_user_id, channel_id):
    return {
    }
'''

def channel_join_v1(auth_user_id, channel_id):
    '''Tests potential error cases'''
    if test_user_is_invalid(auth_user_id):
        raise InputError()
    if test_channel_is_invalid(channel_id):
        raise InputError()
    if not channels[channel_id]['is_public']:
        raise AccessError()

    '''Gets relevant user information'''
    new_user_details = user_details(auth_user_id)
    new_user = {}
    new_user['name_first'] = new_user_details['name_first']
    new_user['name_last'] = new_user_details['name_last']
    new_user['u_id'] = new_user_details['u_id']

    '''Appends to 'all_members' key in dictionary'''
    channels[channel_id]['all_members'].append(new_user)
    return {}


def channel_addowner_v2(token, channel_id, u_id):
    auth_user_id = token_to_id(token)

    if test_channel_is_invalid(auth_user_id):
        raise InputError()
    
    if user_is_owner(u_id):
        raise InputError()

    if not (user_is_owner(auth_user_id) or user_is_owner(auth_user_id)):
        raise AccessError()

    new_owner = {}
    new_owner['u_id'] = u_id
    new_owner['name_first'] = users[u_id]['name_first']
    new_owner['name_last'] = users[u_id]['name_last']
    channels['owner_members'].append = new_owner
    return {
    }

def channel_removeowner_v2(auth_user_id, channel_id, u_id):
    return {
    }


# CUSTOM FUNCTIONS

# Jeffery's functions
# ====================================================================
# looks for token and returns the u_id associated with token
# returns -1 if error
def token_to_id(token):
    if len(users) == 0:
        return -1
    for user in users:
        key, value = 'token', token
        if key in user and value == user[key]:
            return user['u_id']
    return -1

# given a u_id and channel, checks whether they are an owner of the
# channel or not. returns true if they are already owner
def user_is_owner(u_id, channel_id):
    if len(channels[channel_id]['owner_members']) == 0:
        return False
    
    for user in channels[channel_id]['owner_members']:
        key, value = 'u_id', u_id
        if key in user and value == user[key]:
            return True

    return False

# checks if given u_id is the owner of the server Dreams
def user_is_owner(u_id): 
    return users[auth_user_id]['permission_id']

# tests if channel is invalid. 
# returns True if it is; False otherwise
def test_channel_is_invalid(channel_id):
    # if channels list is empty, then obviously invalid
    if len(channels) == 0:
        return True
    # searches for the key value pair of 'id': channel_id
    # if found, then channel exists
    for channel in channels:
        key, value = 'id', channel_id
        if key in channel and value == channel[key]:
            return False

    return True

# tests if user is invalid.
# returns True if it is; False otherwise'''
def test_user_is_invalid(u_id):
    # if users list is empty, then obviously invalid
    if len(users) == 0:
        return True

    # searches for the key value pair of 'u_id': u_id
    # if found, then user exists
    for user in users:
        key, value = 'u_id', u_id
        if key in user and value == user[key]:
            return False

    return True

# tests if user is in a channel.
# returns True if they are
def test_if_user_in_ch(u_id, channel_id):
    # if all_members is empty in given channel, then obviously invalid
    if len(channels[channel_id]['all_members']) == 0:
        return False

    # searches for the key value pair of 'u_id': u_id in all_members within a channel
    # if found, then user is in channel
    for user in channels[channel_id]['all_members']:
        key, value = 'u_id', u_id
        if key in user and value == user[key]:
            return True

    return False

# given a u_id find a user's details and return them as a dict
def user_details(u_id):
    # finds user in users list and returns all details
    for user in users:
        key, value = 'u_id', u_id
        if key in user and value == user[key]:
            return user
    # if user isn't found, then return an empty dict
    return {}
# ====================================================================
