import pytest

from src.auth import auth_register_v2
from src.dm import dm_create_v1, dm_invite_v1, dm_details_v1, dm_list_v1, dm_messages_v1, check_user_in_dm
from src.error import InputError, AccessError
from src.other import clear_v2

def test_invite_basic():
    clear_v2()

    #owner of dm/caller of dm_create
    auth = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')
    auth_token = auth['token']

    #create one user to pass in the list of users for dm create
    user_id = auth_register_v2('test_user@gmail.com', 'test_pw_user', 'userf', 'userl')['auth_user_id']

    #create third user to invite to the dm
    invitee_id = auth_register_v2('test_invitee@gmail.com', 'test_pw_user', 'userf', 'userl')['auth_user_id']

    u_ids = [user_id]
    # create a test dm with two users
    dm_data = dm_create_v1(auth_token, u_ids)

    dm_invite_v1(auth_token, dm_data['dm_id'], invitee_id)

    assert (check_user_in_dm(invitee_id, dm_data['dm_id']))

def test_invite_invalid_dmid():
    clear_v2()

    #owner of dm/caller of dm_create
    auth = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')
    auth_token = auth['token']
    #create third user to invite to the dm
    invitee_id = auth_register_v2('test_invitee@gmail.com', 'test_pw_user', 'userf', 'userl')['auth_user_id']

    #pass invalid dm id to dm invite
    with pytest.raises(InputError):
        dm_invite_v1(auth_token, 10, invitee_id)

def test_invite_invalid_uid():
    clear_v2()

    #owner of dm/caller of dm_create
    auth = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')
    auth_token = auth['token']

    #create one user to pass in the list of users for dm create
    user_id = auth_register_v2('test_user@gmail.com', 'test_pw_user', 'userf', 'userl')['auth_user_id']

    u_ids = [user_id]
    # create a test dm with two users
    dm_data = dm_create_v1(auth_token, u_ids)

    # pass invalid user id to dm_invite
    with pytest.raises(InputError):
        dm_invite_v1(auth_token, dm_data['dm_id'], 4)

def test_invite_not_member():
    clear_v2()

    #owner of dm/caller of dm_create
    auth = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')
    auth_token = auth['token']

    #create one user to pass in the list of users for dm create
    user_id = auth_register_v2('test_user@gmail.com', 'test_pw_user', 'userf', 'userl')['auth_user_id']

    u_ids = [user_id]
    #create third user to invite to the dm
    invitee_id = auth_register_v2('test_invitee@gmail.com', 'test_pw_user', 'userf', 'userl')['auth_user_id']
    #create fourth nonrelevant user 
    spare = auth_register_v2('test_sparee@gmail.com', 'test_pw_user', 'sparef', 'sparel')['token']
    # create a test dm with two users
    dm_data = dm_create_v1(auth_token, u_ids)

    # pass invalid user id to dm_invite
    with pytest.raises(AccessError):
        dm_invite_v1(spare, dm_data['dm_id'], invitee_id)