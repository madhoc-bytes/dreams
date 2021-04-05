from src.channel import test_user_is_invalid, user_details
from src.error import InputError, AccessError
from src.data import dms, users
from src.channel import token_to_id
import jwt
SECRET = 'team'

# dm_create_v1
def dm_create_v1(token, u_ids):
    members = []
    handles = []
    u_id = token_to_id(token)
    if test_user_is_invalid(u_id):
        raise InputError("id from token is invalid")
    for uid in u_ids:
        if test_user_is_invalid(uid):
            raise InputError("id in list is invalid")

    owner_details = user_details(u_id)
    details = {}
    details['u_id'] = owner_details['u_id']
    details['name_first'] = owner_details['name_first']
    details['name_last'] = owner_details['name_last']
    members.append(owner_details)
    handles.append(get_handle_from_uid(u_id))

    for uid in u_ids:
        new_user_details = user_details(uid)
        new_user = {}
        new_user['u_id'] = new_user_details['u_id']
        new_user['name_first'] = new_user_details['name_first']
        new_user['name_last'] = new_user_details['name_last']
        members.append(new_user_details)
        handles.append(get_handle_from_uid(uid))
    dm_id = len(dms)
    dm_name = ", ".join(handles)
    print(dm_name)
    dms.append(
        {
            'dm_id': dm_id,
            'owner_id': get_handle_from_uid(u_id),
            'dm_name': dm_name,
            'all_members': members,
            'messages': []
        }
    )

    return {
        'dm_id': dm_id,
        'dm_name': dm_name
    }


def dm_details_v1(token, dm_id):
    auth_user_id = token_to_id(token)
    # invalid channel
    if test_dm_is_invalid(dm_id):
        raise InputError()

    # invalid user
    if not test_if_user_in_dm(auth_user_id, dm_id):
        raise AccessError()

    # insert info into dictionary and return it
    details = {}
    details['name'] = dms[dm_id]['dm_name']
    details['members'] = dms[dm_id]['all_members']
    return details

def dm_list_v1(token):
    "Function that lists all channels for which a certain user has access"
    auth_user_id = token_to_id(token)
    # Create empty list to store dms details
    dm_details_list = []

    for dm in dms:
        # Check if the user has access to the dm to get details
        if test_if_user_in_dm(auth_user_id, dm['dm_id']):
            dm_details_list.append({
                'name': dm['dm_name'],
                'members': dm['all_members']
            })

    # Return the list
    return {
        'dms': dms_details_list
    }

def dm_invite_v1(token, dm_id, u_id):
    auth_user_id = token_to_id(token)
    # invalid channel
    if test_dm_is_invalid(dm_id):
        raise InputError()

    # invalid user
    if test_user_is_invalid(u_id):
        raise InputError()

    # auth user (inviter) is not already a member of the dm
    if not test_if_user_in_dm(auth_user_id, dm_id):
        raise AccessError()

    # acquiring the details of the user (invitee)
    new_member_details = user_details(u_id)

    # insert user's relevant info (first name, last name and id) into channel's info
    new_member = {}
    new_member['name_first'] = new_member_details['name_first']
    new_member['name_last'] = new_member_details['name_last']
    new_member['u_id'] = new_member_details['u_id']
    dms[dm_id]['all_members'].append(new_member)

    return {}

def dm_messages_v1(token, dm_id, start): 
    '''Tests potential error cases'''
    auth_user_id = token_to_id(token)
    if test_user_is_invalid(auth_user_id):
        raise InputError()
    if test_dm_is_invalid(dm_id):
        raise InputError()
    if not test_if_user_in_dm(auth_user_id, dm_id):
        raise AccessError()
    if start > len(dms[dm_id]['messages']):
        raise InputError()
    '''Appends messages in dm to result, stops when has appended 50 or no more messages'''
    result = []
    i = 0
    for msg in dms[dm_id]['messages']:
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

##############################################################
# Helper functions
def get_handle_from_uid(u_id):
    # finds user in users list 
    for user in users:
        key, value = 'u_id', u_id
        if key in user and value == user[key]:
            return user['handle']
    # if user isn't found, then return an empty dict
    return None

def test_dm_is_invalid(dm_id):
    # if dms list is empty, then obviously invalid
    if len(dms) == 0:
        return True
    # searches for the key value pair of 'id': dm_id
    # if found, then channel exists
    for dm in dms:
        key, value = 'dm_id', dm_id
        if key in dm and value == dm[key]:
            return False
    return True

def test_if_user_in_dm(u_id, dm_id):
    # if all_members is empty in given dm, then obviously invalid
    if len(dms[dm_id]['all_members']) == 0:
        return False

    # searches for the key value pair of 'u_id': u_id in all_members within a dm
    # if found, then user is in dm
    for user in dms[dm_id]['all_members']:
        key, value = 'u_id', u_id
        if key in user and value == user[key]:
            return True
    return False

def check_dm_empty():
    """Function that checks if channel is empty"""
    if len(dms) == 0:
        return True
    return False

def last_dm_id():
    """Function that checks last channel ID"""
    return dms[-1]['dm_id']

def check_if_token_valid(token):
    if not if_token_exit(token) or token == None:
        raise AccessError('Invalid Token')
    return

def if_token_exit(token):
    for user in users:
        if token == user['token']:
            return user
    return False

def importuIDfromtoken(token):
    '''Input a token, return its corresponding u_id''' 
    if len(users) == 0:
        return -1
    for user in users:
        key, value = 'token', token
        if key in user and value == user[key]:
            return user['u_id']
    return -1

