from src.error import InputError, AccessError
from src.data import dms, users
from src.channel import token_to_id
from src.dm import test_dm_is_invalid

def dm_remove_v1(token, dm_id):
    auth_user_id = token_to_id(token)
    if test_dm_is_invalid(dm_id):
        raise InputError()
    if auth_user_id != dms[dm_id]['owner_id']:
        raise AccessError()
    dms.remove(dms[dm_id])

    return {}
