import pytest

from src.auth import auth_register_v2
from src.dm import dm_create_v1, dm_invite_v1, dm_details_v1, dm_list_v1, dm_messages_v1
from src.error import InputError, AccessError
from src.other import clear_v2



def test_dm_messages_nomessage():
    '''Call messages given a dm with no messages'''
    clear_v2()

    #owner of dm/caller of dm_create
    auth = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')
    auth_token = auth['token']
    auth_id = auth['auth_user_id']

    #create one user to pass in the list of users for dm create
    user_id = auth_register_v2('test_user@gmail.com', 'test_pw_user', 'userf', 'userl')['auth_user_id']

    u_ids = [user_id]
    # create a test dm
    dm_data = dm_create_v1(auth_token, u_ids)

    assert dm_messages_v1(auth_token, dm_data['dm_id'], 0) == {
        'messages': [],
        'start': 0,
        'end': -1,
    }

def test_dm_messages_invalid_d_id():
    clear_v2()
    '''Call messages given an invalid dm id'''

    #owner of dm/caller of dm_create
    auth = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')
    auth_token = auth['token']
    auth_id = auth['auth_user_id']
    with pytest.raises(InputError):
        dm_messages_v1(auth_token, 10, 0)

def test_dm_messages_start_too_big():
    '''Call messages given a start > number of messages in dm'''
    clear_v2()

    #owner of dm/caller of dm_create
    auth = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')
    auth_token = auth['token']
    auth_id = auth['auth_user_id']

    #create one user to pass in the list of users for dm create
    user_id = auth_register_v2('test_user@gmail.com', 'test_pw_user', 'userf', 'userl')['auth_user_id']

    u_ids = [user_id]
    # create a test dm
    dm_data = dm_create_v1(auth_token, u_ids)
    
    with pytest.raises(InputError):
        dm_messages_v1(auth_token, dm_data['dm_id'], 1)

def test_dm_messages_not_member():
    '''Call messages given a user not a member of the dm'''
    clear_v2()

    #owner of dm/caller of dm_create
    auth = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')
    auth_token = auth['token']
    auth_id = auth['auth_user_id']

    #create one user to pass in the list of users for dm create
    user_id = auth_register_v2('test_user@gmail.com', 'test_pw_user', 'userf', 'userl')['auth_user_id']

    spare = auth_register_v2('testspare@gmail.com', 'sparepw', 'sparef', 'sparel')['token']
    u_ids = [user_id]
    # create a test dm
    dm_data = dm_create_v1(auth_token, u_ids)
    with pytest.raises(AccessError):
        dm_messages_v1(spare, dm_data['dm_id'], 0)