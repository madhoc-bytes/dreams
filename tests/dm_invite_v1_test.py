''' Test file for dm_invite_v1 '''

from src.dm_invite_v1 import dm_invite_v1
from src.error import InputError, AccessError
from src.data import users, dms
from src.dm_create_v2 import dm_create_v2
from src.other import clear_v1
from src.auth import auth_register_v1

def test_dm_invite():
    clear_v1()

    user_id = auth_register_v1('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['auth_user_id']

    for user in users:
        if user['u_id'] == user_id:
            token = user['token']

    dm_id = dm_create_v2(token, user_id)
    dm_invite_v1(user_id, dm_id, user_id)

    assert is_user_in_dm(user_id, dm_id) == True


def is_user_in_dm(user_id, dm_id):
    exists = False
    for dm in dms:
        if dm_id == dm['dm_id']:
            break 
    for member in dm['all_dm_members']:
        if member['user_id'] == user_id:
            exists = True
    return exists


