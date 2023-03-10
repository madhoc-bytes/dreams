from src.channel import test_user_is_invalid, user_details
from src.error import InputError, AccessError
from src.data import dms, users, dreams
from src.channel import token_to_id
from datetime import datetime, timezone
import jwt
SECRET = 'team'

# dm_create_v1
def dm_create_v1(token, u_ids):
    members = []
    handles = []
    u_id = token_to_id(token)
    # add owner to start of list of ids to be added to dm
    u_ids.insert(0, u_id)

    for uid in u_ids:
        if test_user_is_invalid(uid):
            raise InputError("id in list is invalid")    

    for uid in u_ids:
        new_user_details = user_details(uid)
        new_user = {}
        new_user['u_id'] = new_user_details['u_id']
        new_user['name_first'] = new_user_details['name_first']
        new_user['name_last'] = new_user_details['name_last']
        members.append(new_user)
        handles.append(get_handle_from_uid(uid))
        # user analytics
        time_now = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
        users[uid]['num_dms_joined'] += 1
        users[uid]['timestamp_dm'].append({
            'num_dms_joined': users[uid]['num_dms_joined'],
            'time_stamp': time_now,
        })
    dm_id = len(dms)
    dm_name = ", ".join(handles)
    dms.append(
        {
            'dm_id': dm_id,
            'owner_id': token_to_id(token),
            'dm_name': dm_name,
            'all_members': members,
            'messages': []
        }
    )

    # dreams analytics
    dreams['dms'] += 1
    time_now = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    dreams['timestamp_dm'].append({
        'num_dms_exist': dreams['dms'], 
        'time_stamp': time_now,
    })

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
    if not check_user_in_dm(auth_user_id, dm_id):
        raise AccessError()

    # insert info into dictionary and return it
    details = {}
    details['name'] = dms[dm_id]['dm_name']
    details['members'] = dms[dm_id]['all_members']
    print(details)
    return details

def dm_list_v1(token):
    "Function that lists all channels for which a certain user has access"
    auth_user_id = token_to_id(token)
    # Create empty list to store dms details
    dm_details_list = []

    for dm in dms:
        # Check if the user has access to the dm to get details
        if check_user_in_dm(auth_user_id, dm['dm_id']):
            dm_details_list.append({
                'name': dm['dm_name'],
                'members': dm['all_members']
            })

    print(dm_details_list)
    # Return the list
    return {
        'dms': dm_details_list
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
    if not check_user_in_dm(auth_user_id, dm_id):
        raise AccessError()

    # acquiring the details of the user (invitee)
    new_member_details = user_details(u_id)

    # insert user's relevant info (first name, last name and id) into channel's info
    new_member = {}
    new_member['name_first'] = new_member_details['name_first']
    new_member['name_last'] = new_member_details['name_last']
    new_member['u_id'] = new_member_details['u_id']
    dms[dm_id]['all_members'].append(new_member)
    
    # user analytics
    time_now = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    users[u_id]['num_dms_joined'] += 1
    users[u_id]['timestamp_dm'].append({
        'num_dms_joined': users[u_id]['num_dms_joined'],
        'time_stamp': time_now,
    })

    return {}

def dm_messages_v1(token, dm_id, start): 
    '''Tests potential error cases'''
    auth_user_id = token_to_id(token)
    if test_user_is_invalid(auth_user_id):
        raise InputError()
    if test_dm_is_invalid(dm_id):
        raise InputError()
    if not check_user_in_dm(auth_user_id, dm_id):
        raise AccessError()
    if start > len(dms[dm_id]['messages']):
        raise InputError()
    '''Appends messages in dm to result, stops when has appended 50 or no more messages'''
    result = []
    i = 0
    for msg in dms[dm_id]['messages']:
        if len(msg['reacts']) != 0:
            for react in msg['reacts']:
                if auth_user_id not in react['u_ids']:
                    react['is_this_user_reacted'] = False
                else:
                    react['is_this_user_reacted'] = True

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

def dm_leave_v1(token, dm_id):
    # change the token to a u id
    auth_user_id = token_to_id(token)

    # invalid dm id
    if test_dm_is_invalid(dm_id):
        raise InputError()

    # invalid user
    if not check_user_in_dm(auth_user_id, dm_id):
        raise AccessError() 

    removed = find_user_in_dm(auth_user_id, dm_id)
    dms[dm_id]['all_members'].remove(removed)
    
    # user analytics
    time_now = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    users[auth_user_id]['num_dms_joined'] -= 1
    users[auth_user_id]['timestamp_dm'].append({
        'num_dms_joined': users[auth_user_id]['num_dms_joined'],
        'time_stamp': time_now,
    })   

    return {}

def dm_remove_v1(token, dm_id):
    auth_user_id = token_to_id(token)

    # invalid dm id
    if test_dm_is_invalid(dm_id):
        raise InputError()

    if test_dm_is_invalid(dm_id):
        raise InputError()
    if auth_user_id != dms[dm_id]['owner_id']:
        raise AccessError()
    

    # user analytics
    for member in dms[dm_id]['all_members']:
        time_now = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
        users[member['u_id']]['num_dms_joined'] -= 1
        users[member['u_id']]['timestamp_dm'].append({
            'num_dms_joined': users[member['u_id']]['num_dms_joined'],
            'time_stamp': time_now,
        })    

    # dreams analytics
    dreams['dms'] -= 1
    time_now = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    dreams['timestamp_dm'].append({
        'num_dms_exist': dreams['dms'], 
        'time_stamp': time_now,
    })

    dms.remove(dms[dm_id])
    return {}


##############################################################
# Helper functions
def find_user_in_dm(u_id, dm_id):
    # searches for the key value pair of 'u_id': u_id in all_members within a channel
    # if found, then user is in channel
    for user in dms[dm_id]['all_members']:
        key, value = 'u_id', u_id
        if key in user and value == user[key]:
            return user
    return {}

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

def check_user_in_dm(u_id, dm_id):
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

