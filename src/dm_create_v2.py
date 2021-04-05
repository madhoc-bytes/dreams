from src.channel import token_to_id
from src.error import InputError, AccessError
from src.data import dms, users

def dm_create_v2(token, u_ids):
    token_uid = token_to_id(token)
    user_creator = check_if_user_exit(token_uid)
    handlelist = []
    userlist = []

    for userid in u_ids:
        user = check_if_user_exit(userid)
        if not user:
            raise InputError('userid does not refer to a valid user')
        handlelist.append(user['handle'])
        userlist.append(user)
    new_dm_id = int(len(dms))
    handlelist.sort()
    new_dm_handle = ', '.join(handlelist)

    new_dm = {
        'dm_id': dm_id,
        'creator':user_creator
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
        if user['u_id'] = u_id:
            return user
    return False