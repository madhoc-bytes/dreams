import pytest

from src.data import users, channels, dms
from src.auth import auth_register_v2
from src.dm import dm_create_v1, dm_details_v1, dm_remove_v1
from src.error import InputError, AccessError
from src.other import clear_v2

def test_dm_remove_basic():
    clear_v2()

    #owner of dm/caller of dm_create
    auth = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')
    auth_token = auth['token']

    #create one user to pass in the list of users for dm create
    user_id = auth_register_v2('test_user@gmail.com', 'test_pw_user', 'userf', 'userl')['auth_user_id']

    u_ids = [user_id]
    # create a test dm
    dm_data = dm_create_v1(auth_token, u_ids)
    dm_remove_v1(auth_token, dm_data['dm_id'])
    assert (not check_dm_id_exists(dm_data['dm_id']))

def test_dm_remove_invalid_dmid():
    clear_v2()

    #owner of dm/caller of dm_create
    auth = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')
    auth_token = auth['token']
    with pytest.raises(InputError):
        dm_remove_v1(auth_token, 2)

def test_dm_remove_not_owner():
    clear_v2()

    #owner of dm/caller of dm_create
    auth = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')
    auth_token = auth['token']

    #create one user to pass in the list of users for dm create
    user_id = auth_register_v2('test_user@gmail.com', 'test_pw_user', 'userf', 'userl')
    user_token = user_id['token']
    u_ids = [user_id['auth_user_id']]
    # create a test dm
    dm_data = dm_create_v1(auth_token, u_ids)
    with pytest.raises(AccessError):
        dm_remove_v1(user_token, dm_data['dm_id'])

def check_dm_id_exists(dm_id):
    # if dms list is empty, then obviously invalid
    if len(dms) == 0:
        return False
    # searches for the key value pair of 'id': channel_id
    # if found, then channel exists
    for dm in dms:
        key, value = 'id', dm_id
        if key in dm and value == dm[key]:
            return True
    return False