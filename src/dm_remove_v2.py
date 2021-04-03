from src.error import InputError, AccessError
from src.data import dms,users
import jwt

def dm_remove_v2(token, dm_id):
    if not test_dm_id_is_invalid(dm_id):
        raise InputError('dm_id does not refer to a valid DM')
    #import uid from token
    token_uid = importuIDfromtoken(token)
    if not is_owner_exist(token_uid, dm_id):
         raise AccessError('the user is not the original DM creator')
    remove_dm(token_uid, dm_id)
#helper function
def test_dm_id_is_invalid(dm_id):
    #
    if len(dms) == 0:
        return True
    #
    for dm in dms:
        key, value = 'dm_id', dm_id
        if key in dm and value == dm[key]:
            return False
    return True

def importuIDfromtoken(token):
     '''Input a token, return its corresponding u_id''' 
    u_id_jwt = jwt.decode(token.encode(), SECRET, algorithms=['HS256']) 
    u_id = int(u_id_jwt['u_id'])
    return u_id

def is_owner_exist(u_id, dm_id): 
    for dm in dms: 
        if dm['dm_id'] == dm_id: 
            for owner in dm['owners']: 
                if u_id == owner['u_id']: 
                    return True 
    return False

def remove_dm(u_id, dm_id):
    for dm in dms: 
        if dm['dm_id'] == dm_id: 
            for user in users:
                if u_id == user['u_id']: 
                    dm['owners'].remove(user) 
                    return