'''Imports relevant dictionaries and errors'''
from src.data import users, channels
from src.error import InputError, AccessError

def channel_invite_v1(auth_user_id, channel_id, u_id):
    '''Give two users invite one user into ch_id'''
    if test_channel_is_invalid(channel_id):
        raise InputError()
    if test_user_is_invalid(u_id):
        raise InputError()
    if not test_if_user_in_ch(auth_user_id, channel_id):
        raise AccessError()

    new_member_details = user_details(u_id)
    new_member = {}
    new_member['name_first'] = new_member_details['name_first']
    new_member['name_last'] = new_member_details['name_last']
    new_member['u_id'] = new_member_details['u_id']
    channels[channel_id['id']]['all_members'].append(new_member)

    return {}


def channel_details_v1(auth_user_id, channel_id):
    '''Returns channel details as dictionary'''
    if test_channel_is_invalid(channel_id):
        raise InputError()
    if not test_if_user_in_ch(auth_user_id, channel_id):
        raise AccessError()

    details = {}
    details['name'] = channels[channel_id['id']]['name']
    details['owner_members'] = channels[channel_id['id']]['owner_members']
    details['all_members'] = channels[channel_id['id']]['all_members']

    return details


def channel_messages_v1(auth_user_id, channel_id, start):
    '''Returns all or up to 50 messages in a channel'''
    if test_user_is_invalid(auth_user_id):
        raise InputError()
    if test_channel_is_invalid(channel_id):
        raise InputError()
    if not test_if_user_in_ch(auth_user_id, channel_id):
        raise AccessError()
    if start > len(channels[channel_id['id']]['messages']):
        raise InputError()
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
'''
def channel_leave_v1(auth_user_id, channel_id):
    return {
    }
'''
def channel_join_v1(auth_user_id, channel_id):
    '''Adds a member to 'all_members' key in dictionary'''
    if test_user_is_invalid(auth_user_id):
        raise InputError()
    if test_channel_is_invalid(channel_id):
        raise InputError()
    if not channels[channel_id['id']]['is_public']:
        raise AccessError()

    new_user_details = user_details(auth_user_id)
    new_user = {}
    new_user['name_first'] = new_user_details['name_first']
    new_user['name_last'] = new_user_details['name_last']
    new_user['u_id'] = new_user_details['u_id']

    channels[channel_id['id']]['all_members'].append(new_user)
    return {}

'''
def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }
'''

# CUSTOM FUNCTIONS

# Jeffery's functions
# ====================================================================
def test_channel_is_invalid(channel_id):
    '''Tests if channel is invalid returns True if it is; False otherwise'''
    if len(channels) == 0:
        return True

    for channel in channels:
        key, value = 'id', channel_id['id']
        if key in channel and value == channel[key]:
            return False

    return True

def test_user_is_invalid(u_id):
    '''Tests if user is invalid returns True if it is; False otherwise'''
    if len(users) == 0:
        return True

    for user in users:
        key, value = 'u_id', u_id['auth_user_id']
        if key in user and value == user[key]:
            return False

    return True


def test_if_user_in_ch(u_id, channel_id):
    '''Tests if user is in a channel returns True if they are'''
    if len(channels[channel_id['id']]['all_members']) == 0:
        return False

    for user in channels[channel_id['id']]['all_members']:
        key, value = 'u_id', u_id['auth_user_id']
        if key in user and value == user[key]:
            return True

    return False


def user_details(u_id):
    '''Given a u_id find a user's details and return them as a dict'''
    empty = {}
    if len(users) == 0:
        return empty

    for user in users:
        key, value = 'u_id', u_id['auth_user_id']
        if key in user and value == user[key]:
            return user
# ====================================================================
