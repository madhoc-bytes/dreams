''' File for dm_create_v1 '''

# Imports
from src.channel import test_user_is_invalid
from src.error import InputError, AccessError
from src.data import dms, users, channels
from src.channel import token_to_id
from src.dm_invite_v1 import is_valid_user
import jwt

# dm_create_v1
def dm_create_v1(token, u_ids):
    ''' Function to create a DM '''

    # Get user ID from token
    user_id = token_to_id(token)

    # Check if the user is valid 
    if not is_valid_user(user_id):
        raise InputError('u_id does not refer to a valid user')

    # Check if DM is empty
    if check_dm_empty():
        dm_id = 0
    else:
        dm_id = last_dm_id() + 1
    
    # GET NAME OF DM (!)
    dm_name = ''

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
