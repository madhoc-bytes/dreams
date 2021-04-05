import pytest
from src.data import users, channels, dms
from src.auth import auth_register_v2
from src.dm import dm_create_v1, dm_details_v1
from src.dm_remove import dm_remove_v1
from src.error import InputError, AccessError
from src.other import clear_v2

def test_dm_leave_invalid_dmid():
    clear_v2()

    #owner of dm/caller of dm_create
    auth = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')
    auth_token = auth['token']

    #create one user to pass in the list of users for dm create
    user = auth_register_v2('test_user@gmail.com', 'test_pw_user', 'userf', 'userl')
    user_token = user['token']
    user_id = user['auth_user_id']

    u_ids = [user_id]
    # create a test dm
    dm_create_v1(auth_token, u_ids)

    with pytest.raises(InputError):
        dm_remove_v1(auth_token, 10)

def test_dm_leave_not_member():
    clear_v2()

    #owner of dm/caller of dm_create
    auth = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')
    auth_token = auth['token']

    #create one user to pass in the list of users for dm create
    user = auth_register_v2('test_user@gmail.com', 'test_pw_user', 'userf', 'userl')

    u_ids = []
    # create a test dm
    dm_data = dm_create_v1(auth_token, u_ids)

    with pytest.raises(AccessError):
        dm_remove_v1(user_token, dm_data['dm_id'])