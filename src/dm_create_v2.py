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
        'creator':user
        'dm_name': new_dm_handle,
        'all_dm_members': userlist,
        'messages':[],
    }
    dms.append(new_dm)

    return {
        'dm_id': new_dm_id
        'dm_name': new_dm_handle
    }

def check_if_user_exit(u_id):
    for user in users:
        if user['u_id'] = u_id and user['name_first'] != 'Removed user':
                return user
    return False