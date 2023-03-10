import pytest

from src.auth import auth_register_v2
from src.dm import dm_create_v1, dm_details_v1, dm_invite_v1
from src.error import InputError, AccessError
from src.other import clear_v2

def test_dm_details_basic():    
    clear_v2()

    #owner of dm/caller of dm_create
    auth = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')
    auth_token = auth['token']

    #create one user to pass in the list of users for dm create
    user_id = auth_register_v2('test_user@gmail.com', 'test_pw_user', 'userf', 'userl')['auth_user_id']

    u_ids = [user_id]
    # create a test dm
    dm_data = dm_create_v1(auth_token, u_ids)

    details = dm_details_v1(auth_token, dm_data['dm_id'])

    assert (details['name'] == dm_data['dm_name'])
    assert (details['members'] == [
        {
            'u_id': 0,
            'name_first': 'testf',
            'name_last': 'testl'
        },
        {
            'u_id': 1,
            'name_first': 'userf',
            'name_last': 'userl'
        }
    ])

def test_dm_details_invalid_dmid():    
    clear_v2()

    #owner of dm/caller of dm_create
    auth = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')
    auth_token = auth['token']

    # create a test dm

    with pytest.raises(InputError):
        dm_details_v1(auth_token, 10)

def test_dm_details_not_member():    
    clear_v2()

    #owner of dm/caller of dm_create
    auth = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')
    auth_token = auth['token']

    #create one user to pass in the list of users for dm create
    user_id = auth_register_v2('test_user@gmail.com', 'test_pw_user', 'userf', 'userl')['auth_user_id']

    #create nonrelevant third user 
    spare = auth_register_v2('test_spare@gmail.com', 'test_pw_auth', 'sparetf', 'sparel')
    u_ids = [user_id]
    # create a test dm
    dm_data = dm_create_v1(auth_token, u_ids)

    with pytest.raises(AccessError):
        dm_details_v1(spare, dm_data['dm_id'])
