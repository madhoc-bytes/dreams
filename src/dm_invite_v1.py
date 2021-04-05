''' dm_invite_v1 file'''

# Imports
from src.error import InputError, AccessError
from src.data import dms, users
from src.channel import token_to_id


def dm_invite_v1(token, dm_id, u_id):
    ''' Function that invites user to a DM '''

    if dm_exists(dm_id) == False:
        raise InputError(description='dm_id does not refer to an existing dm.')

    if is_valid_user(u_id) == False:
        raise InputError(description='u_id does not refer to a valid user.')

    if is_user_in_dm(u_id, dm_id) == True:
        raise AccessError(description='the authorised user is not already a member of the DM.')


    for user in users:
        if user['u_id'] == u_id:
            name_first = user['name_first']
            name_last = user['name_last']

    for dm in dms:
        if dm['dm_id'] == dm_id:
            break 

    dm['all_dm_members'].append({
        'u_id': u_id,
        'name_first': name_first,
        'name_last': name_last,
    })

    return {}


def dm_exists(dm_id):
    exists = False
    for dm in dms:
        if dm['dm_id'] == dm_id:
            exists = True
    return exists

def is_valid_user(u_id):
    exists = False 
    for user in users:
        if user['u_id'] == u_id:
            exists = True 
    return exists 


# Function to check if user is in the DM
def is_user_in_dm(user_id, dm_id):
    exists = False
    for dm in dms:
        if dm_id == dm['dm_id']:
            break 
    for member in dm['all_dm_members']:
        if member['u_id'] == user_id:
            exists = True
    return exists