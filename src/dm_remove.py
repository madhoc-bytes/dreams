from src.error import InputError, AccessError
from src.data import dms, users
from src.channel import token_to_id
from src.dm import get_handle_from_uid, test_dm_is_invalid, check_user_in_dm, find_user_in_dm

def dm_remove_v1(token, dm_id):
    auth_user_id = token_to_id(token)
    remover = get_handle_from_uid(auth_user_id)
    # invalid channel
    if test_dm_is_invalid(dm_id):
        raise InputError()

    # invalid user
    if not check_user_in_dm(auth_user_id, dm_id):
        raise AccessError()
    
    removed = find_user_in_dm(auth_user_id, dm_id)
    dms[dm_id]['owner_members'].remove(removed)  

    return{}