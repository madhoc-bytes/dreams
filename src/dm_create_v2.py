from src.channel import test_user_is_invalid, token_to_id
from src.error import InputError, AccessError
from src.data import dms, users

def dm_create_v2(token, u_ids):
    #check valid token#
    check_if_token_valid(token)
    #import uid from token
    token_uid = token_to_id(token)
    #check valid user
    if not test_user_is_invalid(token_uid):
        raise InputError('u_id does not refer to a valid user')
    if check_dm_empty():
        # if dm is empty
        dm_id = 0
    else:
        #last channels id plus 1
        dm_id = last_dm_id() + 1
    dm_name = dm_name.sort()
    new_dm = {
        'dm_id': dm_id,
        'dm_name': dm_name,
        'all_dm_members': [],
    }
    dms.append(new_dm)
    return {
        'dm_id': dm_id,
        'dm_name': dm_name,
    }
    
#helper function#
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
        if token == user[token]:
            return user
    return False