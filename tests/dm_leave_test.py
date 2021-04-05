import pytest

from src.data import users, channels, dms
from src.auth import auth_register_v2
from src.dm import dm_create_v1, dm_details_v1, dm_leave_v1
from src.error import InputError, AccessError
from src.other import clear_v2


def test_dm_leave_basic():
    clear_v2()

    #owner of dm/caller of dm_create
    auth = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')
    auth_token = auth['token']

    #create one user to pass in the list of users for dm create
    user = auth_register_v2('test_user@gmail.com', 'test_pw_user', 'userf', 'userl')
    user_id = user['auth_user_id']
    user_token = user['token']

    u_ids = [user_id]
    # create a test dm
    dm_data = dm_create_v1(auth_token, u_ids)

    # remove user from channel and check if channel has only the first person
    dm_leave_v1(user_token, dm_data['dm_id'])
    details = dm_details_v1(auth_token, dm_data['dm_id'])
    assert (details['members'] == [
        {
            'u_id': 0,
            'name_first': 'testf',
            'name_last': 'testl'
        },
    ])

def test_dm_leave_invalid_dmid():
    clear_v2()

    #owner of dm/caller of dm_create
    auth = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')
    auth_token = auth['token']

    #create one user to pass in the list of users for dm create
    user = auth_register_v2('test_user@gmail.com', 'test_pw_user', 'userf', 'userl')
    user_id = user['auth_user_id']

    u_ids = [user_id]
    # create a test dm
    dm_create_v1(auth_token, u_ids)

    with pytest.raises(InputError):
        dm_leave_v1(auth_token, 10)

def test_dm_leave_not_member():
    clear_v2()

    #owner of dm/caller of dm_create
    auth = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')
    auth_token = auth['token']

    #create one user to pass in the list of users for dm create
    user = auth_register_v2('test_user@gmail.com', 'test_pw_user', 'userf', 'userl')
    user_token = user['token']

    u_ids = []
    # create a test dm
    dm_data = dm_create_v1(auth_token, u_ids)

    with pytest.raises(AccessError):
        dm_leave_v1(user_token, dm_data['dm_id'])

    
