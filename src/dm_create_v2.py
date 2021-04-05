from src.channel import token_to_id, test_user_is_invalid
from src.error import InputError, AccessError
from src.data import dms, users

def dm_create_v2(token, u_ids):
    user = token_to_id(token)
    handlelist = []
    userlist = []

    for userid in u_ids:
        if not test_user_is_invalid(userid):
            raise InputError('userid does not refer to a valid user')
        handlelist.append(user['handle'])
        userlist.append(user)
    new_dm_id = int(len(dms))
    handlelist.sort()
    new_dm_handle = ', '.join(handlelist)

    new_dm = {
        'dm_id': dm_id,
        'dm_name': new_dm_handle,
        'creator':user
        'messages':[],
    }
    dms.append(new_dm)

    return {
        'dm_id': new_dm_id
        'dm_name': new_dm_handle
    }