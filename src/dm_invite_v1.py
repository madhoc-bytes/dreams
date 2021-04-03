''' dm_invite_v1 file'''

from src.error import InputError, AccessError
from src.data import dms, users


def dm_invite_v1(auth_user_id, dm_id, u_id):
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
